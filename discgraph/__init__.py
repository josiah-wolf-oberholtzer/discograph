import mongoengine
from discgraph.models import *


mongodb_client = mongoengine.connect('discgraph')