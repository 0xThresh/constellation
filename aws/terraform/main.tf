data "aws_caller_identity" "current" {}

resource "aws_lexv2models_bot" "constellation_bot" {
  name = "constellation"
  description = ""
  idle_session_ttl_in_seconds = 300
  data_privacy {
    child_directed = false
  }
  role_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-service-role/lexv2.amazonaws.com/AWSServiceRoleForLexV2Bots_F22TKJA8OWV"
}

# V2 Intents aren't available on Terraform yet
# resource "aws_lex_intent" "CheckETHPrice" {
#   name = "CheckETHPrice"
#   description = "Instructs bot to check the price of ETH/USD"
#   sample_utterances = [ 
#     "Check ETH/USD price",
#     "I want to check the price of ETH in USD",
#     "Can you check the price of ETH" 
#     ]

#     fulfillment_activity {
#       type = "ReturnIntent"
#     }
# }
