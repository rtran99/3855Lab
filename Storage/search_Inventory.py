from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class SearchInventory(Base):

    __tablename__ = 'Inventory'
    id = Column(Integer, primary_key=True)
    device_id = Column(String(30),nullable = False)
    trackingId = Column(String(30), nullable=False)
    Itemname = Column(String(20),nullable=False)
    manufacturer = Column(String(30), nullable=False)
    quantity = Column(Integer, nullable = False)
    weight = Column(String(30), nullable=False)
    wishlisted = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)



    def __init__(self,device_id, trackingId, Itemname, manufacturer, quantity, weight,wishlisted):
        self.device_id = device_id
        self.trackingId = trackingId
        self.Itemname = Itemname
        self.manufacturer = manufacturer
        self.quantity = quantity
        self.weight = weight
        self.wishlisted = wishlisted
        self.date_created = datetime.datetime.now()


    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['device_id'] = self.device_id
        dict['trackingId'] = self.trackingId
        dict['Itemname'] = self.Itemname
        dict['manufacturer'] = self.manufacturer
        dict['quantity'] = self.quantity
        dict['weight'] = self.weight
        dict['wishlisted'] = self.wishlisted
        dict['date_created'] = self.date_created


        return dict