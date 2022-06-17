# Description

Icinga2 plugins for checking mails in Mailcow-Quarantine and Mailcow-Mailqueue

# Environment

You need python3 and the pip-package "requests" (pip3 install requests).

# Usage

* **-w / --warn** Number of mails for a WARNING in icinga
* **-c / --crit** Number of mails for a CRITICAL in icinga
* **-a / --apiurl** Full api request URL 
* **-k / --apikey** Api key for your Mailcow




# Icinga2 config

## Comand template
Attention: my checks are located at ```/opt/icinga-checks/``` not in ```PluginDir```

```icinga
object CheckCommand "check_mc_api_quarantine" {
  import "plugin-check-command"
  command = [ "/opt/icinga-checks/check_quara.py" ]
  arguments = {
    "--warn" = "$mcapi_quarantine_warn$"
    "--crit" = "$mcapi_quarantine_crit$"
    "--apiurl" = "$mcapi_quarantine_apiurl$"
    "--apikey" = "$mcapi_quarantine_apikey$"
  }
}
```
```icinga
object CheckCommand "check_mc_api_mailqueue" {
  import "plugin-check-command"
  command = [ "/opt/icinga-checks/check_mailqueue.py" ]
  arguments = {
    "--warn" = "$mcapi_mailqueue_warn$"
    "--crit" = "$mcapi_mailqueue_crit$"
    "--apiurl" = "$mcapi_mailqueue_apiurl$"
    "--apikey" = "$mcapi_mailqueue_apikey$"
  }
}
```
## Service template

```icinga
apply Service for (check_mc_api_quarantine => config in host.vars.check_mc_api_quarantine) {
        import "generic-service"
        check_command = "check_mc_api_quarantine"
        vars += config
}
```
```icinga
apply Service for (check_mc_api_mailqueue => config in host.vars.check_mc_api_mailqueue) {
        import "generic-service"
        check_command = "check_mc_api_mailqueue"
        vars += config
}
```

## Host object
Just add both vars to your Mailcow host-object
```icinga
vars.check_mc_api_quarantine["mailcow-quarantine"] = {
    mcapi_quarantine_warn = 1
    mcapi_quarantine_crit = 10
    mcapi_quarantine_apiurl = "https://YOURCOW/api/v1/get/quarantine/all"
    mcapi_quarantine_apikey = "YOUR API KEY"
}
```
```icinga
vars.check_mc_api_mailqueue["mailcow-mailqueue"] = {
    mcapi_mailqueue_warn = 1
    mcapi_mailqueue_crit = 10
    mcapi_mailqueue_apiurl = "https://YOURCOW/api/v1/get/mailq/all"
    mcapi_mailqueue_apikey = "YOUR API KEY"
}
```



