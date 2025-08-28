curl "https://gpt.byteintl.net/faas-api-test/v1/chat/completions" -H "Content-Type: application/json; charset=utf-8" -H "Authorization: Bearer empty" -d '{
  "messages": [
    {
      "role": "system",
      "content": "You are codewise, a helpful assistant built for TikTok Generalized Arch Team."
    },
    {
      "role": "user",
      "content": "如何用ReactLynx实现带定时器的倒计时组件？需要后台线程处理倒计时逻辑"
    }
  ],  
  "stream": false,  
  "temperature": 0.4,
  "model": "codewise_32b_staging"
}'


