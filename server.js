const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// 정적 파일 제공
app.use(express.static(__dirname));

// 메인 라우트
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'data-workshop-site.html'));
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`🚀 Server is running on port ${PORT}`);
  console.log(`📱 Local: http://localhost:${PORT}`);
});
