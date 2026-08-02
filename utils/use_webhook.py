def use_webhook(config):
    use_wh = config.get("Webhook_URL", False) and config.get("Result_Webhook", False)

    return use_wh
