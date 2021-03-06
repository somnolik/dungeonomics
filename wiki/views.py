from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView

from . import models
from . import forms


@login_required
def wiki_home(request, section_pk=None, subsection_pk=None):
    sections = sorted(models.Section.objects.all(),
        key=lambda section: section.order)

    subsections = []
    for section in sections:
        subsections.append(sorted(
            models.Subsection.objects.filter(section=section),
            key=lambda subsection: subsection.order
            ))
    subsections = [item for sublist in subsections for item in sublist]

    if section_pk:
        this_section = get_object_or_404(models.Section, pk=section_pk)
        this_subsections = sorted(models.Subsection.objects.filter(section=this_section),
        key=lambda subsection: subsection.order)
        if subsection_pk:
            this_subsection = get_object_or_404(models.Subsection, pk=subsection_pk)
        else:
            this_subsection = None

        if this_subsection:
            return render(request, 'wiki/home.html', {'this_section': this_section, 'this_subsection': this_subsection, 'sections': sections, 'subsections': subsections})
        else:
            return render(request, 'wiki/home.html', {'this_section': this_section, 'sections': sections, 'subsections': subsections})
    else:
        this_section = None
        sections = sorted(models.Section.objects.all(),
            key=lambda section: section.order)
        if len(sections) > 0:
            this_section = sections[0]
        return render(request, 'wiki/home.html', {'this_section': this_section, 'sections': sections, 'subsections': subsections})

@staff_member_required
def section_create(request):
    form = forms.SectionForm()
    if request.method == 'POST':
        form = forms.SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.save()
            messages.add_message(request, messages.SUCCESS, "Section created!")
            return HttpResponseRedirect(section.get_absolute_url())
    return render(request, 'wiki/section_form.html', {'form': form})

@staff_member_required
def subsection_create(request, section_pk):
    section = get_object_or_404(models.Section, pk=section_pk)
    form = forms.SubsectionForm()
    if request.method == 'POST':
        form = forms.SubsectionForm(request.POST)
        if form.is_valid():
            subsection = form.save(commit=False)
            subsection.section = section
            subsection.save()
            messages.add_message(request, messages.SUCCESS, "Subsection created!")
            return HttpResponseRedirect(subsection.get_absolute_url())
    return render(request, 'wiki/subsection_form.html', {'form': form, 'section': section})

@staff_member_required
def section_update(request, section_pk):
    section = get_object_or_404(models.Section, pk=section_pk)
    form = forms.SectionForm(instance=section)
    if request.method == 'POST':
        form = forms.SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Updated section: {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect(section.get_absolute_url())
    return render(request, 'wiki/section_form.html', {'form': form, 'section': section})

@staff_member_required
def subsection_update(request, section_pk, subsection_pk):
    subsection = get_object_or_404(models.Subsection, pk=subsection_pk, section_id=section_pk)
    form = forms.SubsectionForm(instance=subsection)
    if request.method == 'POST':
        form = forms.SubsectionForm(request.POST, instance=subsection)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Updated subsection: {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect(subsection.get_absolute_url())
    return render(request, 'wiki/subsection_form.html', {'form': form, 'section': subsection.section, 'subsection': subsection})


class SectionDelete(LoginRequiredMixin, DeleteView):
    model = models.Section
    success_url = reverse_lazy('wiki:home')
    slug_field = "pk"
    slug_url_kwarg = "section_pk"

    def delete(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        else:
            messages.add_message(self.request, messages.SUCCESS, "Section deleted!")
            return super(SectionDelete, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        section = super(SectionDelete, self).get_object()
        return section

class SubsectionDelete(LoginRequiredMixin, DeleteView):
    model = models.Subsection
    success_url = reverse_lazy('wiki:home')
    slug_field = "pk"
    slug_url_kwarg = "subsection_pk"

    def delete(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        else:
            messages.add_message(self.request, messages.SUCCESS, "Subsection deleted!")
            return super(SubsectionDelete, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        subsection = super(SubsectionDelete, self).get_object()
        return subsection