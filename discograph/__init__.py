import mongoengine
from discograph import bootstrap
from discograph import models


mongodb_client = mongoengine.connect('discograph')