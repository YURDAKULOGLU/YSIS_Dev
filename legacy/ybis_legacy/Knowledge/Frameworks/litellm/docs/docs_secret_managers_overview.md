Secret Managers Overview | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

info

✨ **This is an Enterprise Feature**

[Enterprise Pricing](https://www.litellm.ai/#pricing)

[Contact us here to get a free trial](https://calendly.com/d/4mp-gd3-k5k/litellm-1-1-onboarding-chat)

LiteLLM supports **reading secrets (eg. `OPENAI_API_KEY`)** and **writing secrets (eg. Virtual Keys)** from Azure Key Vault, Google Secret Manager, Hashicorp Vault, CyberArk Conjur, and AWS Secret Manager.

## Supported Secret Managers[​](#supported-secret-managers "Direct link to Supported Secret Managers")

* [AWS Key Management Service](/docs/secret_managers/aws_kms)
* [AWS Secret Manager](/docs/secret_managers/aws_secret_manager)
* [Azure Key Vault](/docs/secret_managers/azure_key_vault)
* [CyberArk Conjur](/docs/secret_managers/cyberark)
* [Google Secret Manager](/docs/secret_managers/google_secret_manager)
* [Google Key Management Service](/docs/secret_managers/google_kms)
* [Hashicorp Vault](/docs/secret_managers/hashicorp_vault)

## All Secret Manager Settings[​](#all-secret-manager-settings "Direct link to All Secret Manager Settings")

All settings related to secret management

```
general_settings:  
  key_management_system: "aws_secret_manager" # REQUIRED  
  key_management_settings:    
  
    # Storing Virtual Keys Settings  
    store_virtual_keys: true # OPTIONAL. Defaults to False, when True will store virtual keys in secret manager  
    prefix_for_stored_virtual_keys: "litellm/" # OPTIONAL.I f set, this prefix will be used for stored virtual keys in the secret manager  
      
    # Access Mode Settings  
    access_mode: "write_only" # OPTIONAL. Literal["read_only", "write_only", "read_and_write"]. Defaults to "read_only"  
      
    # Hosted Keys Settings  
    hosted_keys: ["litellm_master_key"] # OPTIONAL. Specify which env keys you stored on AWS  
  
    # K/V pairs in 1 AWS Secret Settings  
    primary_secret_name: "litellm_secrets" # OPTIONAL. Read multiple keys from one JSON secret on AWS Secret Manager
```

## Team-Level Secret Manager Settings[​](#team-level-secret-manager-settings "Direct link to Team-Level Secret Manager Settings")

Team-level secret manager settings let every team bring their own key-management configuration. These settings are used when creating virtual keys tied to the team.

Follow these steps to configure it:

1. **Create a team**  
   Open the Teams page and click `Create Team` to launch the modal.

   ![](/assets/ideal-img/secret_manager_settings_create_team.e721fc2.640.png)
2. **Expand Additional Settings**  
   Use the `Additional Settings` toggle to reveal the advanced configuration panel.

![](/assets/ideal-img/secret_manager_settings_additional_settings.9ffe028.640.png)

3. **Configure the Secret Manager**  
   In the `Secret Manager Settings` panel, paste the provider-specific JSON. Refer to each provider page (AWS, Azure, Google, Hashicorp, etc.) for the supported keys/values. JSON is required today, but we plan to add a more UI-friendly editor.

   ![](/assets/ideal-img/secret_manager_settings.ce8808f.640.png)
4. **Create the team**  
   Review the inputs and click `Create Team` to save.

   ![](/assets/ideal-img/secret_manager_settings_create_button.b098aea.640.png)

Once saved, LiteLLM will use this configuration.

* [Supported Secret Managers](#supported-secret-managers)
* [All Secret Manager Settings](#all-secret-manager-settings)
* [Team-Level Secret Manager Settings](#team-level-secret-manager-settings)