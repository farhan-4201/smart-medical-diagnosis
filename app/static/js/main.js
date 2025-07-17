// AI Doctor - Enhanced Frontend JavaScript

class AIDoctorApp {
    constructor() {
        this.currentFile = null;
        this.currentAudio = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupDragAndDrop();
        this.checkBrowserSupport();
    }
    
    setupEventListeners() {
        // File upload
        const fileInput = document.getElementById('imageInput');
        const uploadArea = document.getElementById('uploadArea');
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }
        
        if (uploadArea) {
            uploadArea.addEventListener('click', () => fileInput?.click());
        }
        
        // Form submission
        const diagnosisForm = document.getElementById('diagnosisForm');
        if (diagnosisForm) {
            diagnosisForm.addEventListener('submit', (e) => this.handleDiagnosisSubmit(e));
        }
        
        // Audio recording
        const recordBtn = document.getElementById('recordBtn');
        const stopBtn = document.getElementById('stopBtn');
        
        if (recordBtn) {
            recordBtn.addEventListener('click', () => this.startRecording());
        }
        
        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopRecording());
        }
        
        // Audio playback
        const playAudioBtn = document.getElementById('playAudioBtn');
        if (playAudioBtn) {
            playAudioBtn.addEventListener('click', () => this.playAudioResponse());
        }
    }
    
    setupDragAndDrop() {
        const uploadArea = document.getElementById('uploadArea');
        if (!uploadArea) return;
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('drag-active');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('drag-active');
            }, false);
        });
        
        uploadArea.addEventListener('drop', (e) => this.handleDrop(e), false);
    }
    
    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            this.handleFile(files[0]);
        }
    }
    
    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.handleFile(file);
        }
    }
    
    handleFile(file) {
        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            this.showAlert('Please select a valid image file (JPEG, PNG, or WebP)', 'error');
            return;
        }
        
        // Validate file size (5MB)
        const maxSize = 5 * 1024 * 1024;
        if (file.size > maxSize) {
            this.showAlert('File size must be less than 5MB', 'error');
            return;
        }
        
        this.currentFile = file;
        this.displayImagePreview(file);
        this.updateUploadArea(file.name);
    }
    
    displayImagePreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById('imagePreview');
            if (preview) {
                preview.innerHTML = `
                    <img src="${e.target.result}" alt="Preview" 
                         style="max-width: 200px; max-height: 200px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                `;
                preview.classList.remove('hidden');
            }
        };
        reader.readAsDataURL(file);
    }
    
    updateUploadArea(filename) {
        const uploadArea = document.getElementById('uploadArea');
        const uploadText = document.getElementById('uploadText');
        
        if (uploadText) {
            uploadText.innerHTML = `
                <div class="flex items-center justify-center gap-2">
                    <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                    <span class="font-medium text-green-700">File selected: ${filename}</span>
                </div>
                <p class="text-sm text-gray-500 mt-1">Click to change file</p>
            `;
        }
        
        if (uploadArea) {
            uploadArea.style.borderColor = '#22c55e';
            uploadArea.style.backgroundColor = 'rgba(34, 197, 94, 0.05)';
        }
    }
    
    async handleDiagnosisSubmit(e) {
        e.preventDefault();
        
        if (!this.currentFile) {
            this.showAlert('Please select an image first', 'error');
            return;
        }
        
        const symptoms = document.getElementById('symptoms')?.value || '';
        
        this.showLoading(true);
        this.clearResults();
        
        try {
            const formData = new FormData();
            formData.append('file', this.currentFile);
            if (symptoms) {
                formData.append('symptoms', symptoms);
            }
            
            const response = await fetch('/api/diagnosis/analyze', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            this.displayResults(result);
            
            // Generate audio response
            if (result.diagnosis) {
                await this.generateAudioResponse(result.diagnosis);
            }
            
        } catch (error) {
            console.error('Analysis failed:', error);
            this.showAlert('Analysis failed. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    displayResults(result) {
        const resultsSection = document.getElementById('resultsSection');
        if (!resultsSection) return;
        
        resultsSection.innerHTML = `
            <div class="card diagnosis-result">
                <div class="card-header">
                    <h3 class="text-xl font-bold text-blue-700 flex items-center gap-2">
                        <svg class="w-6 h-6 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        Analysis Complete
                    </h3>
                </div>
                <div class="card-body">
                    <div class="mb-4">
                        <h4 class="font-semibold text-gray-700 mb-2">Diagnosis:</h4>
                        <p class="text-gray-800 leading-relaxed">${result.diagnosis}</p>
                    </div>
                    
                    <div class="mb-4">
                        <h4 class="font-semibold text-gray-700 mb-2">Confidence Level:</h4>
                        <div class="confidence-meter">
                            <div class="confidence-fill" style="width: ${result.confidence}%"></div>
                        </div>
                        <p class="text-sm text-gray-600 mt-1">${result.confidence}% confidence</p>
                    </div>
                    
                    <div class="mb-4">
                        <h4 class="font-semibold text-gray-700 mb-2">Recommended Actions:</h4>
                        <p class="text-gray-800 leading-relaxed">${result.solution}</p>
                    </div>
                    
                    <div id="audioResponseSection" class="audio-controls hidden">
                        <h4>Audio Response</h4>
                        <div class="flex items-center gap-3">
                            <button id="playAudioBtn" class="btn btn-primary btn-sm">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>
                                </svg>
                                Play Audio Response
                            </button>
                            <audio id="audioPlayer" controls class="hidden"></audio>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        resultsSection.classList.remove('hidden');
        
        // Setup audio playback
        const playBtn = document.getElementById('playAudioBtn');
        if (playBtn) {
            playBtn.addEventListener('click', () => this.playAudioResponse());
        }
    }
    
    async generateAudioResponse(text) {
        try {
            const formData = new FormData();
            formData.append('text', text);
            
            const response = await fetch('/api/diagnosis/audio-response', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const audioBlob = await response.blob();
                const audioUrl = URL.createObjectURL(audioBlob);
                
                const audioPlayer = document.getElementById('audioPlayer');
                const audioSection = document.getElementById('audioResponseSection');
                
                if (audioPlayer && audioSection) {
                    audioPlayer.src = audioUrl;
                    audioSection.classList.remove('hidden');
                }
            }
        } catch (error) {
            console.error('Audio generation failed:', error);
        }
    }
    
    playAudioResponse() {
        const audioPlayer = document.getElementById('audioPlayer');
        const playBtn = document.getElementById('playAudioBtn');
        
        if (audioPlayer && audioPlayer.src) {
            audioPlayer.classList.remove('hidden');
            audioPlayer.play();
            
            if (playBtn) {
                playBtn.textContent = 'Playing...';
                playBtn.disabled = true;
                
                audioPlayer.onended = () => {
                    playBtn.innerHTML = `
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>
                        </svg>
                        Play Audio Response
                    `;
                    playBtn.disabled = false;
                };
            }
        }
    }
    
    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                this.currentAudio = audioBlob;
                this.displayAudioPreview(audioBlob);
                
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            this.updateRecordingUI(true);
            
            // Auto-stop after 30 seconds
            setTimeout(() => {
                if (this.isRecording) {
                    this.stopRecording();
                }
            }, 30000);
            
        } catch (error) {
            console.error('Recording failed:', error);
            this.showAlert('Microphone access denied or unavailable', 'error');
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.updateRecordingUI(false);
        }
    }
    
    updateRecordingUI(recording) {
        const recordBtn = document.getElementById('recordBtn');
        const stopBtn = document.getElementById('stopBtn');
        const recordingIndicator = document.getElementById('recordingIndicator');
        
        if (recording) {
            recordBtn?.classList.add('hidden');
            stopBtn?.classList.remove('hidden');
            recordingIndicator?.classList.remove('hidden');
        } else {
            recordBtn?.classList.remove('hidden');
            stopBtn?.classList.add('hidden');
            recordingIndicator?.classList.add('hidden');
        }
    }
    
    displayAudioPreview(audioBlob) {
        const audioPreview = document.getElementById('audioPreview');
        if (audioPreview) {
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPreview.innerHTML = `
                <div class="flex items-center gap-3">
                    <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                    <span class="text-green-700 font-medium">Audio recorded successfully</span>
                </div>
                <audio controls src="${audioUrl}" class="mt-2 w-full"></audio>
            `;
            audioPreview.classList.remove('hidden');
        }
    }
    
    showLoading(show) {
        const loadingElement = document.getElementById('loadingIndicator');
        const submitBtn = document.getElementById('submitBtn');
        
        if (show) {
            loadingElement?.classList.remove('hidden');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        Analyzing...
                    </div>
                `;
            }
        } else {
            loadingElement?.classList.add('hidden');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = `
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Get Diagnosis
                `;
            }
        }
    }
    
    clearResults() {
        const resultsSection = document.getElementById('resultsSection');
        if (resultsSection) {
            resultsSection.classList.add('hidden');
            resultsSection.innerHTML = '';
        }
    }
    
    showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alertContainer');
        if (!alertContainer) return;
        
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${type}`;
        alertElement.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="text-current opacity-75 hover:opacity-100">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                    </svg>
                </button>
            </div>
        `;
        
        alertContainer.appendChild(alertElement);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertElement.parentElement) {
                alertElement.remove();
            }
        }, 5000);
    }
    
    checkBrowserSupport() {
        // Check for required APIs
        const features = {
            fileAPI: window.File && window.FileReader,
            mediaRecorder: window.MediaRecorder,
            getUserMedia: navigator.mediaDevices && navigator.mediaDevices.getUserMedia
        };
        
        const unsupported = Object.entries(features)
            .filter(([name, supported]) => !supported)
            .map(([name]) => name);
        
        if (unsupported.length > 0) {
            this.showAlert(
                `Your browser doesn't support: ${unsupported.join(', ')}. Some features may not work.`,
                'warning'
            );
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AIDoctorApp();
});

// Service Worker registration for PWA capabilities
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}