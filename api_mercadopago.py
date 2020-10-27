import os, sys
import mercadopago
import json

def payment(req, **kwargs):
    product = kwargs["product"]    
    preference = {
      "items": [
        {
          "title": "Coffee Test",
          "quantity": 1,
          "currency_id": "CLP",
          "unit_price": product.price
        }
      ]
    }

    mp = mercadopago.MP("TEST-7211265184697033-092819-f0b63b9f417525939baab82275bb2d4e-652326753")

    preferenceResult = mp.preference.create(preference)

    url = preferenceResult["response"]["init_point"]
