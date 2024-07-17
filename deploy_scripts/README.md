These scripts help deploy specific instances of MST5.

If you want to make sure that these deployments are not affected the by system restart, add the following to `crontab -e`:

```bash
@reboot bash deploy_scripts/deploy-mst5-qald9plus-dbpedia.sh
@reboot bash deploy_scripts/deploy-mst5-qald9plus-wikidata.sh
@reboot bash deploy_scripts/deploy-mst5-qald9plus-testeval-wikidata.sh
```