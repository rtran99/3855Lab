from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class PlaceShipment(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True)
    device_id = Column(String(30), nullable=False)
    shippingPriority = Column(String(30), nullable=False)
    shippingCompany = Column(String(30), nullable=False)
    address = Column(String(50), nullable=False)
    name = Column(String(20), nullable=False)
    deliveryDate = Column(String(30), nullable=False)
    ordersreceived = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self,device_id,shippingPriority,shippingCompany,address,name,deliveryDate,ordersreceived):
        self.device_id = device_id
        self.shippingPriority = shippingPriority
        self.shippingCompany = shippingCompany
        self.address = address
        self.name = name
        self.deliveryDate = deliveryDate
        self.ordersreceived = ordersreceived
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['device_id'] = self.device_id
        dict['shippingPriority'] = self.shippingPriority
        dict['shippingCompany'] = self.shippingCompany
        dict['address'] = self.address
        dict['name'] = self.name
        dict['deliveryDate'] = self.deliveryDate
        dict['ordersreceived'] = self.ordersreceived
        dict['date_created'] = self.date_created

        return dict
