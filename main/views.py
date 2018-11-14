from django.shortcuts import render
from django.http import JsonResponse
from .models import WordFile, Word, WordType
from django.views.decorators.csrf import csrf_exempt
import openpyxl


@csrf_exempt
def word_plus(req):
    if req.method == 'POST':
        req_data = req.POST
        word_file = WordFile(file=req.FILES['file'])
        word_file.save()
        wb = openpyxl.load_workbook("media/" + word_file.file.name)
        ws = wb.active

        if req_data['type'] == '1':
            word_type = WordType.objects.get(pk=1)
        elif req_data['type'] == '2':
            word_type = WordType.objects.get(pk=2)

        for r in ws.rows:
            word: str = r[1].value.strip().replace('.', '')
            if word.find('(') != -1:
                word = word[:word.find('(')] + word[word.find(')') + 1:]

            if len(word) <= 1 or Word.objects.filter(type=word_type).filter(text=word).exists():
                continue
            if r[2].value is None:
                word_temp = Word(type=word_type, text=word, info='', rank=0)
            else:
                word_temp = Word(type=word_type, text=word, info=r[2].value, rank=0)
            word_temp.save()

        return JsonResponse({'success': True})


