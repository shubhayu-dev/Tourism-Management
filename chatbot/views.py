from django.shortcuts import render
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

def index(request):
    return render(request, 'chatbot/index.html')

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        inputs = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')
        attention_mask = torch.ones(inputs.shape, device= device)
        outputs = model.generate(
            inputs.to(device), attention_mask= attention_mask, max_length= 1000,
            pad_token_id= tokenizer.eos_token_id,
        )
        response = tokenizer.decode(outputs[:,inputs.shape[-1]:][0], skip_special_tokens=True)
        
        return JsonResponse({'response': response})
    