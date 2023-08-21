from app.settings import app_settings


def anti_captcha_configured() -> bool:
    return len(app_settings.anti_captcha_com_apikey) > 0


real_captcha_image_base64 = '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'
