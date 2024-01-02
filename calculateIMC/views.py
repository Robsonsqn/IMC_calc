from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def process_data(request):
    if request.method == 'POST':
        altura = float(request.POST.get('altura').replace(',','.'))
        peso = float(request.POST.get('peso'))

        IMC = peso / (pow(altura,2))
        
        if(IMC < 18.5):
            categoria = 'Abaixo do Peso'
        elif(IMC >= 18.5 and IMC <= 24.99):
            categoria = 'Peso Normal'
        elif(IMC >= 25 and IMC <= 29.99):
            categoria = 'Sobrepeso'
        elif(IMC >= 30 and IMC <= 34.99):
            categoria = 'Obesidade'
        elif(IMC >= 35 and IMC <= 39.99):
            categoria = 'Obesidade Grau II'
        else:
            categoria = 'Obesidade Grau III'

        data = {'IMC': round(IMC,2), 'Categoria': categoria, 'Peso': peso, 'Altura':altura}
        print(data)

        return JsonResponse(data)

def enviar_email(request):
    if request.method == 'POST':
        corpo_email = render(request, 'email_template.html', {
            'IMC': request.POST.get('IMC'),
            'Categoria': request.POST.get('Categoria'),
        }).content.decode('utf-8')

        destinatario = request.POST.get('destinatario')
        assunto = 'Dados do IMC'
        print(destinatario)
        try:
            send_mail(
                assunto,
                '',
                settings.EMAIL_HOST_USER,
                [destinatario],
                fail_silently=False,
                html_message=corpo_email,
            )
            return JsonResponse({'mensagem': 'E-mail enviado com sucesso!'})
        except Exception as e:
            print(e)
            return JsonResponse({'erro': str(e)}, status=500)