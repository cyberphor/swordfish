source .env

# Request an API key. 
curl -X POST http://localhost:4010/api/api-key \
  -k \
  --cert ${EMASS_API_CERTIFICATE} \
  --key ${EMASS_API_KEY} \
  -H "user-uid: ${EMASS_USER_UID}" \
  -H "api-key: ${EMASS_API_KEY}"

echo ""
