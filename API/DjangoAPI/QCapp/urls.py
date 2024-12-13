from django.urls import path
from QCapp import views

urlpatterns = [
    path('projects/', views.projectsApi),
    path('projects/<int:id>/', views.projectsApi),
    path('batches/', views.batchesApi),
    path('batches/<int:id>/', views.batchesApi),
    path('groups/', views.GroupsApi),
    path('groups/<int:id>/', views.GroupsApi),
    path('samples/', views.samplesApi),
    path('samples/<int:id>/', views.samplesApi),
    path('metabolites/', views.MetabolitesApi),
    path('metabolites/<int:id>/', views.MetabolitesApi),
    path('metabolite_conc/', views.Metabolite_concApi),
    path('metabolite_conc/<int:id>/', views.Metabolite_concApi),
    
    path('pca_plot/', views.generate_pca_plot, name='pca_plot'),
    
    path('table_samples/', views.generate_table_samples, name='table_samples'),
    path('table_cal_qc/', views.generate_table_cal_qc, name='table_cal_qc'),
    path('table_labqc/', views.generate_table_labqc, name='table_labqc'),
    
    path('missing_counts/', views.generate_missing_counts, name='missing_values'),
    
    path('generate_cal_plots/', views.generate_cal_plots, name='generate_cal_plots'),
    path('get_cal_plot/<int:plot_number>/', views.get_cal_plot, name='get_cal_plot'),
    
    path('generate_cal_intra_projects_plots/', views.generate_cal_intra_projects_plots, name='generate_cal_intra_projects_plots'),
    path('get_cal_intra_projects_plot/<int:plot_number>/', views.get_cal_intra_projects_plot, name='get_cal_intra_projects_plot'),
    
    path('generate_qc_plots/', views.generate_qc_plots, name='generate_qc_plots'),
    path('get_qc_plot/<int:plot_number>/', views.get_qc_plot, name='get_qc_plot'),
    
    path('generate_intra_qc_plots/', views.generate_intra_qc_plots, name='generate_intra_qc_plots'),
    path('get_intra_qc_plots/<int:plot_number>/', views.get_intra_qc_plots, name='get_intra_qc_plots'),
    
    path('generate_labqc_plots/', views.generate_labqc_plots, name='generate_labqc_plots'),
    path('get_labqc_plot/', views.get_labqc_plot, name='get_labqc_plot'),
    
    path('generate_intra_labqc_plots/', views.generate_intra_labqc_plots, name='generate_intra_labqc_plots'),
    path('get_intra_labqc_plot/', views.get_intra_labqc_plot, name='get_intra_labqc_plot')
]
