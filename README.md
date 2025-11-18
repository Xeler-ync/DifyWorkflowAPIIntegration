# DifyWorkflowAPIIntegration

## Sentiment Analysis
```bash
cd sentiment_analysis
mkdir models
cd models
git clone https://huggingface.co/uer/roberta-base-finetuned-jd-binary-chinesef
```

## torch
```bash
# If you are using a GPU, you can install the GPU version of PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
# If you are using a CPU, you can install the CPU version of PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```