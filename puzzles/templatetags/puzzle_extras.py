from django import template
from puzzles.models import Puzzle, MetaPuzzle
from puzzles.forms import StatusForm
from answers.forms import AnswerForm

register = template.Library()

@register.inclusion_tag('puzzles_table.html')
def get_table(puzzles, request):
    status_forms = [StatusForm(initial={'status': p.status}) for p in puzzles]
    for (i, p) in enumerate(puzzles):
        if p.status in [Puzzle.SOLVED, Puzzle.PENDING]:
            status_forms[i].fields["status"].disabled = True

    answer_form = AnswerForm()
    return {'rows': zip(puzzles, status_forms), 'guess_form': answer_form}


@register.inclusion_tag('title.html')
def get_title(puzzle):
    badge = ''
    if MetaPuzzle.objects.filter(pk=puzzle.pk).exists():
        badge = 'META'
    return {'puzzle': puzzle, 'badge': badge}


@register.simple_tag
def puzzle_class(puzzle):
    if puzzle.status == Puzzle.PENDING:
        return "table-warning"
    elif puzzle.status == Puzzle.SOLVED:
        return "table-success"
    elif puzzle.status == Puzzle.STUCK:
        return "table-danger"
    else:
        return ""