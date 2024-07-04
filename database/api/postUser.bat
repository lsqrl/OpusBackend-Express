@echo off
@echo off
curl -X POST http://localhost:5000/insertUser -H "Content-Type: application/json" -d "{\"role_id\": \"Both\", \"wallet_address\": \"0123456789abcdef0123\", \"name\": \"Hermione Granger\", \"password\": \"alohom_ora\", \"address\": \"8 Heathgate, Hampstead Garden Suburb, London\", \"age\": 18, \"gender\": \"Female\", \"email\": \"hermione.granger@hogwarts.mag\", \"kyc_aml_id\": \"1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef\"}"
pause
