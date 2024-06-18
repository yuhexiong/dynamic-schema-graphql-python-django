import yaml

def get_mysql_connection(cfg_path):
	db_connection = {
		'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': None,
		'USER': None,
		"PASSWORD": None,
		'HOST': None, }}
	
	with open(cfg_path, 'r')as fp:
		cfg = yaml.safe_load(fp)
		
	db_connection['default']['NAME'] = cfg.get("name")
	db_connection['default']['USER'] = cfg.get("user")
	db_connection['default']["PASSWORD"] = cfg.get("password")
	db_connection['default']["HOST"] = cfg.get("host")
	db_connection['default']["PORT"] = cfg.get("port")
		
	return db_connection