import logging

flails_logger = logging.getLogger('FlailsLogger')
flails_logger_handler = logging.FileHandler('flails.log')
flails_logger_handler.setFormatter(logging.Formatter("%(asctime)s :: %(message)s"))
flails_logger.addHandler(flails_logger_handler)
flails_logger.setLevel(logging.INFO)
