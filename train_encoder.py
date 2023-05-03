import argparse
import pandas as pd
import torch
import transformers
from torch.utils.data import DataLoader, Dataset
from transformers import XLMWithLMHeadModel, XLMTokenizer

# Define custom dataset for training data
class CustomDataset(Dataset):
    def __init__(self, df, tokenizer):
        self.df = df
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        text = self.df.iloc[index]['text']
        summary = self.df.iloc[index]['summary']

        inputs = self.tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")
        labels = self.tokenizer(summary, padding=True, truncation=True, max_length=128, return_tensors="pt")

        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': labels['input_ids'].squeeze()
        }

def main(args):
    # Load pre-trained XLM model and tokenizer
    model = XLMWithLMHeadModel.from_pretrained('facebook/xlm-v-base')
    tokenizer = XLMTokenizer.from_pretrained('facebook/xlm-v-base')

    # Load CSV file with training data
    train_df = pd.read_csv(args.train_csv)

    # Create custom dataset and dataloader for training data
    train_dataset = CustomDataset(train_df, tokenizer)
    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=args.per_device_train_batch_size)

    # Fine-tune model with training data
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.num_train_epochs)

    training_args = {
        'per_device_train_batch_size': args.per_device_train_batch_size,
        'gradient_accumulation_steps': args.gradient_accumulation_steps,
        'output_dir': args.output_dir,
        'save_steps': args.save_steps,
        'save_total_limit': args.save_total_limit,
        'report_to': args.report_to,
        'gradient_checkpointing': args.gradient_checkpointing,
        'evaluation_strategy': 'epoch',
        'learning_rate': args.learning_rate,
        'num_train_epochs': args.num_train_epochs,
        'warmup_steps': args.warmup_steps,
        'weight_decay': args.weight_decay
    }

    if torch.cuda.is_available():
        training_args['fp16'] = {'enabled': args.fp16}

    trainer = transformers.Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=lambda data: {'input_ids': torch.stack([item['input_ids'] for item in data]),
                                    'attention_mask': torch.stack([item['attention_mask'] for item in data]),
                                    'labels': torch.stack([item['labels'] for item in data])},
        optimizers=(optimizer, None),
        scheduler=scheduler,
        device='cuda' if torch.cuda.is_available() else 'cpu',
        callbacks=[transformers.logging.TensorBoardCallback(log_dir='./logs')]
    )

    trainer.train()

    # Save fine-tuned model
    model.save_pretrained(args.output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--train_csv", type=str, required=True, help="Path to the training CSV file with columns 'text' and 'summary'.")
    parser.add_argument("--output_dir", type=str, default="fine_tuned_xlm", help="Path to the directory to save the fine-tuned model.")
    parser.add_argument("--per_device_train_batch_size", type=int, default=8, help="Batch size for training.")
    parser.add_argument("--learning_rate", type=float, default=5e-5, help="Learning rate for the optimizer.")
    parser.add_argument("--num_train_epochs", type=int, default=10, help="Number of training epochs.")
    parser.add_argument("--warmup_steps", type=int, default=500, help="Number of warmup steps.")
    parser.add_argument("--weight_decay", type=float, default=0.01, help="Weight decay for the optimizer.")
    parser.add_argument("--save_steps", type=int, default=500, help="Save model checkpoint every N steps.")
    parser.add_argument("--save_total_limit", type=int, default=5, help="Maximum number of model checkpoints to save.")
    parser.add_argument("--gradient_checkpointing", action="store_true", help="Enable gradient checkpointing to save memory.")
    parser.add_argument("--gradient_accumulation_steps", type=int, default=2, help="Number of gradient accumulation steps.")
   
