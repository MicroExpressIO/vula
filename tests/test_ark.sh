curl https://ark-ap-southeast.byteintl.net/api/v3/chat/completions   -H "Content-Type: application/json"   -H "Authorization: Bearer 7385c60a-2ba0-45c4-8bc6-06d655719ad3"   -d '{
    "model": "ep-20250624013439-l6tv9",
    "messages": [
      {"role": "system","content": "You are a security advisor"},
      {"role": "user","content": "[60772]Debian Security Update for less (DLA 3823-1)"}
    ]
  }'

  