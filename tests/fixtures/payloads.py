# tests/fixtures/payloads.py

import json

# Valid Status Update Payload
VALID_STATUS_UPDATE_PAYLOAD = json.dumps({
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "entry_id_1",
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15550000000",
                            "phone_number_id": "phone_number_id_1"
                        },
                        "statuses": [
                            {
                                "id": "status_id_1",
                                "status": "delivered",
                                "timestamp": "1627773291",
                                "recipient_id": "15551234567",
                                "conversation": {
                                    "id": "conversation_id_1",
                                    "origin": {
                                        "type": "service"
                                    }
                                },
                                "pricing": {
                                    "billable": True,
                                    "pricing_model": "CBP",
                                    "category": "service"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
})

# Valid Text Message Payload
VALID_TEXT_MESSAGE_PAYLOAD = json.dumps({
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "entry_id_2",
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15550000000",
                            "phone_number_id": "phone_number_id_1"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Alice"
                                },
                                "wa_id": "15551234567"
                            }
                        ],
                        "messages": [
                            {
                                "from": "15551234567",
                                "id": "message_id_1",
                                "timestamp": "1627771715",
                                "text": {
                                    "body": "Hello, this is a test message."
                                },
                                "type": "text"
                            }
                        ]
                    }
                }
            ]
        }
    ]
})

# Valid Document Message Payload
VALID_DOCUMENT_MESSAGE_PAYLOAD = json.dumps({
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "entry_id_3",
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15550000000",
                            "phone_number_id": "phone_number_id_1"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Bob"
                                },
                                "wa_id": "15557654321"
                            }
                        ],
                        "messages": [
                            {
                                "from": "15557654321",
                                "id": "message_id_2",
                                "timestamp": "1627773047",
                                "type": "document",
                                "document": {
                                    "filename": "test_document.pdf",
                                    "mime_type": "application/pdf",
                                    "sha256": "fake_sha256_hash_value",
                                    "id": "document_id_1"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
})


# Valid List Reply Message: 
VALID_LIST_REPLY = json.dumps({
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "102290129340398",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15550783881",
              "phone_number_id": "106540352242922"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Pablo Morales"
                },
                "wa_id": "16505551234"
              }
            ],
            "messages": [
              {
                "context": {
                  "from": "15550783881",
                  "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBIwMjg0RkMxOEMyMkNEQUFFRDgA"
                },
                "from": "16505551234",
                "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgASGBQzQTZDMzFGRUFBQjlDMzIzMzlEQwA=",
                "timestamp": "1712595443",
                "type": "interactive",
                "interactive": {
                  "type": "list_reply",
                  "list_reply": {
                    "id": "priority_express",
                    "title": "Priority Mail Express",
                    "description": "Next Day to 2 Days"
                  }
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
})




# Invalid Payload Example: Missing 'type' field in message
INVALID_MESSAGE_PAYLOAD = json.dumps({
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "entry_id_4",
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15550000000",
                            "phone_number_id": "phone_number_id_1"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Charlie"
                                },
                                "wa_id": "15559876543"
                            }
                        ],
                        "messages": [
                            {
                                "from": "15559876543",
                                "id": "message_id_3",
                                "timestamp": "1627771715",
                                "text": {
                                    "body": "This message lacks a type field."
                                }
                                # 'type' field is missing here
                            }
                        ]
                    }
                }
            ]
        }
    ]
})


INTERACTIVE_LIST_SEND_PAYLOAD = json.dumps({
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "header": {
      "type": "text",
      "text": "Choose Shipping Option"
    },
    "body": {
      "text": "Which shipping option do you prefer?"
    },
    "footer": {
      "text": "Lucky Shrub: Your gateway to succulents™"
    },
    "action": {
      "button": "Shipping Options",
      "sections": [
        {
          "title": "I want it ASAP!",
          "rows": [
            {
              "id": "priority_express",
              "title": "Priority Mail Express",
              "description": "Next Day to 2 Days"
            },
            {
              "id": "priority_mail",
              "title": "Priority Mail",
              "description": "1–3 Days"
            }
          ]
        },
        {
          "title": "I can wait a bit",
          "rows": [
            {
              "id": "usps_ground_advantage",
              "title": "USPS Ground Advantage",
              "description": "2–5 Days"
            },
            {
              "id": "media_mail",
              "title": "Media Mail",
              "description": "2–8 Days"
            }
          ]
        }
      ]
    }
  }
})