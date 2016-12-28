from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Question, Choice


# Create your views here.

def index(request):

	latest_question_list = Question.objects.order_by('-pub_date')[:5]
		
	context = {
		'latest_question_list': latest_question_list,
	}
	
	return render(request, 'polls/index.html', context)
	
	
def about(request):

	author_dict = {
		"Sun Tzu": "The supreme art of war is to subdue the enemy without fighting.", 
		"Mandela": "I learned that courage was not the absence of fear, but the triumph over it. The brave man is not he who does not feel afraid, but he who conquers that fear.", 
		"Gandhi": "Strength does not come from physical capacity. It comes from an indomitable will."}
		
	author_pics_dict = {
		"Sun Tzu": "http://larrygeorges-productions.co.nf/Website%20Experience/image/sun%20tzu.jpg", 
		"Mandela": "http://larrygeorges-productions.co.nf/Website%20Experience/image/mandela.png", 
		"Gandhi": "http://larrygeorges-productions.co.nf/Website%20Experience/image/gandhi_2.jpg"}
	
	context = {
		'author_dict': author_dict,
		'author_pics_dict': author_pics_dict
	}

	return render(request, 'polls/about.html', context)
	
	
def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', context={'question': question})
	

def result(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})
	

def vote(request, question_id):

	question = get_object_or_404(Question, pk=question_id)
	
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	
	
	except (KeyError, Choice.DoesNotExist):
		#Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	
	
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#Always return an HttpResponseRedirect after successfully dealing
		#with POST data. This prevents data from being posted twice if a 
		#user hits the back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))