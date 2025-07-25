from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-colors',
                'rows': 6,
                'placeholder': 'Write a compelling cover letter explaining why you are the best candidate for this position...'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-colors',
                'accept': '.pdf,.doc,.docx'
            })
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size (max 5MB)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Resume file size must be less than 5MB.')
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = resume.name.lower()
            if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError('Please upload a PDF, DOC, or DOCX file.')
        
        return resume

    def clean_cover_letter(self):
        cover_letter = self.cleaned_data.get('cover_letter')
        if cover_letter:
            if len(cover_letter) < 50:
                raise forms.ValidationError('Cover letter must be at least 50 characters long.')
            if len(cover_letter) > 2000:
                raise forms.ValidationError('Cover letter must be no more than 2000 characters.')
        
        return cover_letter 