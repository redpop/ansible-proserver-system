# ansible-proserver-system
An Ansible role that sets up a Proserver system.

### Features
| Variable name | Default value | Description |
| ------------- | ------------- | ----------- |
| `system.features.authorized_keys_delete` | no | Whether the public keys that aren't managed by Ansible should be removed from the target host. When this variable is set to `yes`, removing a key from the variables will remove it from the target host during the next run. |
| `system.features.users_delete` | no | Whether removing a user from the variables should automatically remove them from the target hosts. Please note that you need to have ran the playbook at least once beforehand, so that Ansible can create a list of current users.

