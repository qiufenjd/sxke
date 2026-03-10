
// 全局状态变量
let selectedFile = null;
let startTime = null;
let timerInterval = null;

// 

// 文件选择事件处理
document.getElementById('file-input').addEventListener('change', function(e) {
    handleFiles(e.target.files);
});

// 拖放事件处理
function handleDragOver(e) {
    e.preventDefault();
    document.getElementById('drop-zone').classList.add('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    document.getElementById('drop-zone').classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
}

// 文件处理核心逻辑
function handleFiles(files) {
    const errorArea = document.getElementById('error-area');
    errorArea.classList.add('hidden');
    
    if (files.length > 0) {
        selectedFile = files[0];
        
        // 验证文件类型
        if (!selectedFile.type.startsWith('audio/')) {
            showError('仅支持音频文件格式');
            selectedFile = null;
            return;
        }

        document.getElementById('file-info').innerHTML = `
            <p>文件名：${selectedFile.name}</p>
            <p>大小：${(selectedFile.size/1024/1024).toFixed(2)}MB</p>
        `;
    }
}

// 转换进度更新
function updateProgress(percentage) {
    const progressBar = document.getElementById('progress-bar');
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-text');
    
    progressBar.classList.remove('hidden');
    progressFill.style.width = `${percentage}%`;
    progressText.textContent = `${Math.round(percentage)}%`;
}

// 转换启动函数
function startConversion() {
    const convertBtn = document.getElementById('convert-btn');
    const timerElement = document.getElementById('timer');
    const timeCounter = document.getElementById('time-counter');
    
    // 重置状态
    timerElement.classList.remove('hidden');
    document.getElementById('error-area').classList.add('hidden');
    document.getElementById('download-area').classList.add('hidden');
    convertBtn.disabled = true;
    convertBtn.querySelector('.loading-dots').classList.remove('hidden');

    // 验证文件
    if (!selectedFile) {
        showError('请先选择音频文件');
        convertBtn.disabled = false;
        return;
    }

    // 清除旧定时器
    if (timerInterval) clearInterval(timerInterval);
    
    // 启动新计时器
    startTime = Date.now();
    timerInterval = setInterval(() => {
        const seconds = Math.floor((Date.now() - startTime) / 1000);
        timeCounter.textContent = seconds;
    }, 1000);

    // 准备表单数据
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('format', document.getElementById('format-select').value);
    formData.append('speed', document.getElementById('speed').value);

    updateProgress(0);

    // 发送请求
    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error(`服务器错误: ${response.status}`);
        return response.json();
    })
    .then(data => {
        if (data.error) throw new Error(data.error);
        showDownloadLink(data.download_url);
        updateProgress(100);
    })
    .catch(error => {
        showError(error.message);
        updateProgress(0);
    })
    .finally(() => {
        clearInterval(timerInterval);
        timerInterval = null;
        convertBtn.disabled = false;
        convertBtn.querySelector('.loading-dots').classList.add('hidden');
        
        // 显示最终时间
        if (startTime) {
            const finalTime = Math.floor((Date.now() - startTime) / 1000);
            timeCounter.textContent = finalTime;
        }
    });
}

// 下载链接显示
function showDownloadLink(url) {
    const downloadArea = document.getElementById('download-area');
    downloadArea.innerHTML = `
        <a href="${url}" class="download-btn" download>
            ↓ 下载转换文件
        </a>
    `;
    downloadArea.classList.remove('hidden');
}

// 错误显示
function showError(message) {
    const errorArea = document.getElementById('error-area');
    errorArea.innerHTML = `
        <div class="error-alert">
            <span class="error-icon">⚠</span>
            <p class="error-message">${message}</p>
        </div>
    `;
    errorArea.classList.remove('hidden');
}

// 速度值显示
function updateSpeedValue(value) {
    document.getElementById('speed-value').textContent = `${value}x`;
}