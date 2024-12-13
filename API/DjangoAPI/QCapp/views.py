from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use('Agg')
from io import BytesIO
import json
import scipy.stats as ss
import matplotlib.cm as cm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import os

from .models import Projects, Batches, Samples, Groups, Metabolites, Metabolites_conc
from .serializers import ProjectsSerializer, BatchesSerializer, SamplesSerializer, GroupsSerializer, MetabolitesSerializer, Metabolites_concSerializer


current_dir = os.path.dirname(__file__)
print(current_dir)
ref_qc_data_file = os.path.join(current_dir, 'Ref_QC_data.xlsx')

@csrf_exempt
def projectsApi(request, id=0):
    if request.method == 'GET':
        project_id = request.GET.get('project_id')
        project_name = request.GET.get('project_name')
        id = request.GET.get('id')

        if project_id and project_name:
            projects = Projects.objects.filter(project_id=project_id, project_name=project_name)
        elif project_id:
            projects = Projects.objects.filter(project_id=project_id)
        elif project_name:
            projects = Projects.objects.filter(project_name=project_name)
        elif id:
            projects = Projects.objects.filter(id=id)
        else:
            projects = Projects.objects.all()

        projects_serializer = ProjectsSerializer(projects, many=True)
        return JsonResponse(projects_serializer.data, safe=False)

    elif request.method == 'POST':
        project_data = JSONParser().parse(request)
        project_serializer = ProjectsSerializer(data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse("Project added Successfully!!", safe=False)
        return JsonResponse("Failed to add project.", safe=False)
    elif request.method == 'PUT':
        project_data = JSONParser().parse(request)
        project = Projects.objects.get(id=id)
        project_serializer = ProjectsSerializer(project, data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse("Project updated Successfully!!", safe=False)
        return JsonResponse("Failed to update project.", safe=False)
    elif request.method == 'DELETE':
        project = Projects.objects.get(id=id)
        project.delete()
        return JsonResponse("Project deleted Successfully!!", safe=False)

@csrf_exempt
def batchesApi(request, id=0):
    if request.method == 'GET':
        project_id = request.GET.get('project_id')
        batch_num = request.GET.get('batch_num')
        id=request.GET.get('id')

        if project_id and batch_num:
            batches = Batches.objects.filter(project_id=project_id, batch_num=batch_num)
        elif project_id:
            batches = Batches.objects.filter(project_id=project_id)
        elif batch_num:
            batches = Batches.objects.filter(batch_num=batch_num)
        elif id:
            batches = Batches.objects.filter(id=id)
        else:
            batches = Batches.objects.all()

        batches_serializer = BatchesSerializer(batches, many=True)
        return JsonResponse(batches_serializer.data, safe=False)

    elif request.method == 'POST':
        batch_data = JSONParser().parse(request)
        batch_serializer = BatchesSerializer(data=batch_data)
        if batch_serializer.is_valid():
            batch_serializer.save()
            return JsonResponse("Batch added Successfully!!", safe=False)
        return JsonResponse("Failed to add batch.", safe=False)
    elif request.method == 'PUT':
        batch_data = JSONParser().parse(request)
        batch = Batches.objects.get(id=batch_data['id'])
        batch_serializer = BatchesSerializer(batch, data=batch_data)
        if batch_serializer.is_valid():
            batch_serializer.save()
            return JsonResponse("Batch updated Successfully!!", safe=False)
        return JsonResponse("Failed to update batch.", safe=False)
    elif request.method == 'DELETE':
        batch = Batches.objects.get(id=id)
        batch.delete()
        return JsonResponse("Batch deleted Successfully!!", safe=False)


@csrf_exempt
def GroupsApi(request, id=0):
    if request.method == 'GET':
        id = request.GET.get('id')
        group_name = request.GET.get('group_name')

        if id and group_name:
            groups = Groups.objects.filter(id=id, group_name=group_name)
        elif id:
            groups = Groups.objects.filter(id=id)
        elif group_name:
            groups = Groups.objects.filter(group_name=group_name)
        else:
            groups = Groups.objects.all()

        groups_serializer = GroupsSerializer(groups, many=True)
        return JsonResponse(groups_serializer.data, safe=False)  # safe=False makes sure that the output is not a dictionary

    if request.method == 'POST':
        sample_type_data = JSONParser().parse(request)
        sample_type_serializer = GroupsSerializer(data=sample_type_data)
        if sample_type_serializer.is_valid():
            sample_type_serializer.save()  # Remove the id parameter
            return JsonResponse("Sample type added Successfully!!", safe=False)
        return JsonResponse("Failed to add sample type.", safe=False)
    elif request.method == 'PUT':
        sample_type_data = JSONParser().parse(request)
        sample_type = Groups.objects.get(id=sample_type_data['id'])
        sample_type_serializer = GroupsSerializer(sample_type, data=sample_type_data)
        if sample_type_serializer.is_valid():
            sample_type_serializer.save()
            return JsonResponse("Sample type updated Successfully!!", safe=False)
        return JsonResponse("Failed to update sample type.", safe=False)
    elif request.method == 'DELETE':
        sample_type = Groups.objects.get(id=id)
        sample_type.delete()
        return JsonResponse("Sample type deleted Successfully!!", safe=False)


@csrf_exempt
def samplesApi(request, id=0):
    if request.method == 'GET':
        batch_id = request.GET.get('batch_id')
        sample_name = request.GET.get('sample_name')
        project_id = request.GET.get('project_id')
        
        if project_id and batch_id and sample_name:
            samples = Samples.objects.filter(project_id=project_id, batch_id=batch_id, sample_name=sample_name)
        elif project_id and batch_id:
            samples = Samples.objects.filter(project_id=project_id, batch_id=batch_id)
        elif project_id:
            samples = Samples.objects.filter(project_id=project_id)
        elif batch_id and sample_name:
            samples = Samples.objects.filter(batch_id=batch_id, sample_name=sample_name)
        elif batch_id:
            samples = Samples.objects.filter(batch_id=batch_id)
        elif sample_name:
            samples = Samples.objects.filter(sample_name=sample_name)
            
        else:
            samples = Samples.objects.all()
        samples_serializer = SamplesSerializer(samples, many=True)
        return JsonResponse(samples_serializer.data, safe=False)
    elif request.method == 'POST':
        sample_data = JSONParser().parse(request)
        sample_serializer = SamplesSerializer(data=sample_data)
        if sample_serializer.is_valid():
            sample_serializer.save()
            return JsonResponse("Sample added Successfully!!", safe=False)
        return JsonResponse("Failed to add sample.", safe=False)
    elif request.method == 'PUT':
        sample_data = JSONParser().parse(request)
        sample = Samples.objects.get(id=sample_data['id'])
        sample_serializer = SamplesSerializer(sample, data=sample_data)
        if sample_serializer.is_valid():
            sample_serializer.save()
            return JsonResponse("Sample updated Successfully!!", safe=False)
        return JsonResponse("Failed to update sample.", safe=False)
    elif request.method == 'DELETE':
        sample = Samples.objects.get(id=id)
        sample.delete()
        return JsonResponse("Sample deleted Successfully!!", safe=False)
    
@csrf_exempt
def MetabolitesApi(request, id=0):
    if request.method == 'GET':
        metabolite_name = request.GET.get('metabolite_name')
        if metabolite_name:
            metabolites = Metabolites.objects.filter(metabolite_name=metabolite_name)
        else:
            metabolites = Metabolites.objects.all()
        Metabolites_serializer = MetabolitesSerializer(metabolites, many=True)
        return JsonResponse(Metabolites_serializer.data, safe=False)
    elif request.method == 'POST':
        Metabolites_data = JSONParser().parse(request)
        Metabolites_serializer = MetabolitesSerializer(data=Metabolites_data)
        if Metabolites_serializer.is_valid():
            Metabolites_serializer.save()
            return JsonResponse("Metabolite added Successfully!!", safe=False)
        return JsonResponse("Failed to add Metabolite.", safe=False)
    elif request.method == 'PUT':
        Metabolites_data = JSONParser().parse(request)
        metabolites = Metabolites.objects.get(id=Metabolites_data['id'])
        Metabolites_serializer = MetabolitesSerializer(Metabolites, data=Metabolites_data)
        if Metabolites_serializer.is_valid():
            Metabolites_serializer.save()
            return JsonResponse("Metabolite updated Successfully!!", safe=False)
        return JsonResponse("Failed to update Metabolite.", safe=False)
    elif request.method == 'DELETE':
        metabolites = Metabolites.objects.get(id=id)
        metabolites.delete()
        return JsonResponse("Metabolite deleted Successfully!!", safe=False)

@csrf_exempt
def Metabolite_concApi(request, id=0):
    if request.method == 'GET':
        metabolite_id = request.GET.get('metabolite_id')
        sample_id = request.GET.get('sample_id')
        if metabolite_id and sample_id:
            metabolite_conc = Metabolites_conc.objects.filter(metabolite_id=metabolite_id, sample_id=sample_id)
        elif metabolite_id:
            metabolite_conc = Metabolites_conc.objects.filter(metabolite_id=metabolite_id)
        elif sample_id:
            metabolite_conc = Metabolites_conc.objects.filter(sample_id=sample_id)
        else:
            metabolite_conc = Metabolites_conc.objects.all()
        metabolite_conc_serializer = Metabolites_concSerializer(metabolite_conc, many=True)
        return JsonResponse(metabolite_conc_serializer.data, safe=False)
    elif request.method == 'POST':
        Metabolite_conc_data = JSONParser().parse(request)
        Metabolite_conc_serializer = Metabolites_concSerializer(data=Metabolite_conc_data)
        if Metabolite_conc_serializer.is_valid():
            Metabolite_conc_serializer.save()
            return JsonResponse("Metabolite_conc added Successfully!!", safe=False)
        return JsonResponse("Failed to add Metabolite_conc.", safe=False)
    elif request.method == 'PUT':
        Metabolite_conc_data = JSONParser().parse(request)
        Metabolite_conc = Metabolites_conc.objects.get(id=Metabolite_conc_data['id'])
        Metabolite_conc_serializer = Metabolites_concSerializer(Metabolite_conc, data=Metabolite_conc_data)
        if Metabolite_conc_serializer.is_valid():
            Metabolite_conc_serializer.save()
            return JsonResponse("Metabolite_conc updated Successfully!!", safe=False)
        return JsonResponse("Failed to update Metabolite_conc.", safe=False)
    elif request.method == 'DELETE':
        Metabolite_conc = Metabolites_conc.objects.get(id=id)
        Metabolite_conc.delete()
        return JsonResponse("Metabolite_conc deleted Successfully!!", safe=False)


@csrf_exempt
def generate_pca_plot(request):
    if request.method == 'POST':
        # Get the uploaded data from the request
        data = json.loads(request.body)

        # Convert the data to a Pandas dataframe
        data = pd.DataFrame(list(data.values())[0])
        
        # Exclude from Group column rows with Cal and QC
        data = data[~data['Group'].isin(['Cal', 'QC'])] 

        # Perform data cleaning and preprocessing
        data_PCA = data.drop(['Sample', 'Group'], axis=1)

        # Replace missing values with the median of each column, but only for numeric columns
        for col in data_PCA.columns:
            if pd.api.types.is_numeric_dtype(data_PCA[col]):
                data_PCA[col] = data_PCA[col].fillna(data_PCA[col].median())

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data_PCA)

        # Apply PCA transformation
        pca = PCA(n_components=2)
        pca_data = pca.fit_transform(scaled_data)

        # Create a plot
        fig, ax = plt.subplots(figsize=(10,12))

        # Remove the white frames around the plot
        fig.patch.set_facecolor('none')
        ax.patch.set_facecolor('none')

        # Color by groups
        unique_groups = np.unique(data['Group'])
        colors = cm.get_cmap('tab10', len(unique_groups))

        for i, group in enumerate(unique_groups):
            group_scores = pca_data[data['Group'] == group]
            ax.scatter(group_scores[:, 0], group_scores[:, 1], color=colors(i), label=group, s=150)  # Increase the size of the points

            # Annotate for number
            for j, number in enumerate(data.index[data['Group'] == group]):
                ax.annotate(number, (group_scores[j, 0], group_scores[j, 1]), color=colors(i), fontsize=17)  # Increase the font size of the annotations

        # Calculate Hotelling's T2
        a = 0.95
        n = len(pca_data)
        p = len(pca_data[0])
        f = ss.f.ppf(a, p, n - p)
        sx = np.std(pca_data[:, 0])
        sy = np.std(pca_data[:, 1])
        m = [np.pi * x / 100.0 for x in range(200)]
        cx = np.cos(m) * sx * f
        cy = np.sin(m) * sy * f

        ax.plot(cx, cy, '--', color='#a8005c', label='Hotelling T2 95%', linewidth=2)  # Increase the line width of the Hotelling's T2 plot

        ax.set_xlabel('PC1', fontsize=20)  # Increase the font size of the x-axis label
        ax.set_ylabel('PC2', fontsize=20)  # Increase the font size of the y-axis label
        ax.legend(loc='best', fontsize=15)  # Increase the font size of the legend
        ax.tick_params(axis='both', labelsize=20)  # Increase the font size of the tick labels

        # Save the plot to a buffer
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)  # Use bbox_inches='tight' and pad_inches=0 to remove the white frames around the plot
        buf.seek(0)

        # Return the plot as an image response
        return HttpResponse(buf.getvalue(), content_type='image/png')

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

@csrf_exempt
def generate_table_samples(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        df = pd.DataFrame(data)
        metabolites = df.columns[3:]
        grouped = df.groupby('Group')
        results = []

        for group_name, group_df in grouped:
            if group_name not in ["labQC", "Cal", "QC"]:
                row_sums = group_df[metabolites].sum(axis=1)
                Q1 = np.percentile(row_sums, 25)
                Q3 = np.percentile(row_sums, 75)
                IQR = Q3 - Q1
                lower_bound_1_5 = Q1 - 1.5 * IQR
                upper_bound_1_5 = Q3 + 1.5 * IQR
                lower_bound_3 = Q1 - 3 * IQR
                upper_bound_3 = Q3 + 3 * IQR

                res = []
                for value in row_sums:
                    if lower_bound_1_5 <= value <= upper_bound_1_5:
                        res.append('passed')
                    elif lower_bound_3 < value < lower_bound_1_5 or upper_bound_1_5 < value < upper_bound_3:
                        res.append('semi_passed')
                    else:
                        res.append('not_passed')

                group_results = pd.DataFrame({'group': group_name[:2], 'sample_name': group_df['Sample'], 'level': res})
                results.extend(group_results.to_dict(orient='records'))

        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def generate_table_cal_qc(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        df = pd.DataFrame(data)
        data_ref = pd.read_excel(ref_qc_data_file, sheet_name='References')
        calibrators = {}
        qcs = {}
        for i in range(6):
            calibrators[i] = []
            for index, row in df.iterrows():
                if row['Sample'] == f'Cal-{i+1}':
                    for metabolite in df.columns:
                        if metabolite not in ['__EMPTY', 'Sample', 'Group']:
                            value = row[metabolite]
                            lower = data_ref.loc[i, metabolite] * (1 - data_ref['Accepted'][i])
                            upper = data_ref.loc[i, metabolite] * (1 + data_ref['Accepted'][i])
                            if value <= lower:
                                result = 'low'
                            elif value >= upper:
                                result = 'high'
                            else:
                                result = 'passed'
                            calibrators[i].append({'metabolite': metabolite, 'result': result})

        for j, qc in enumerate(['LQC', 'MQC', 'HQC']):
            qcs[qc] = []
            for index, row in df.iterrows():
                if row['Group'] == 'QC' and qc in row['Sample']:
                    for metabolite in df.columns:
                        if metabolite not in ['__EMPTY', 'Sample', 'Group']:
                            value = row[metabolite]
                            lower=data_ref.loc[j+6,metabolite]*(1-0.15)
                            upper=data_ref.loc[j+6,metabolite]*(1+0.15)
                            if value <= lower:
                                result = 'low'
                            elif value >= upper:
                                result = 'high'
                            else:
                                result = 'passed'
                            qcs[qc].append({'metabolite': metabolite, 'result': result})

        metabolites = [col for col in df.columns if col not in ['__EMPTY', 'Sample', 'Group']]
        result = []
        for metabolite in metabolites:
            calibrator_results = []
            for i in range(6):
                if i in calibrators:
                    for item in calibrators[i]:
                        if item['metabolite'] == metabolite:
                            calibrator_results.append(item['result'])
            qc_results = {}
            for qc in qcs:
                qc_result = []
                for item in qcs[qc]:
                    if item['metabolite'] == metabolite:
                        qc_result.append(item['result'])
                qc_results[qc.lower()] = qc_result
            result.append({
                'name': metabolite,
                'calibrators': calibrator_results,
                'lqc': qc_results.get('lqc', []),
                'mqc': qc_results.get('mqc', []),
                'hqc': qc_results.get('hqc', [])
            })

        result_json = json.dumps(result)

        return HttpResponse(result_json, content_type='application/json')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def generate_table_labqc(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        df = pd.DataFrame(data_json)

        # Filter the data to only include rows where the 'Group' is 'labQC'
        df_labqc = df[df['Group'] == 'labQC']

        data_ref = pd.read_excel(ref_qc_data_file, sheet_name='References')

        metabolites_names = df_labqc.columns[3:]

        result = []
        for metabolite in metabolites_names:
            ref_low = data_ref[metabolite][10]
            ref_very_low = data_ref[metabolite][11]
            ref_high = data_ref[metabolite][12]
            ref_very_high = data_ref[metabolite][13]
            levels = []
            for index, row in df_labqc.iterrows():
                
                value = row[metabolite]
                if value >= ref_very_high:
                    levels.append('high')
                elif value < ref_very_high and value >= ref_high:
                    levels.append('semi_high')
                elif value < ref_high and value > ref_low:
                    levels.append('passed')
                elif value <= ref_low and value > ref_very_low:
                    levels.append('semi_low')
                elif value <= ref_very_low:
                    levels.append('low')
                else:
                    levels.append('unknown')
            result.append({
                'name': metabolite,
                'labqc': levels
            })

        return JsonResponse(result, safe=False)
    
@csrf_exempt
def generate_missing_counts(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        df = pd.DataFrame(data_json)

        missing_counts = df.groupby('Group').apply(lambda x: x.isnull().sum())

        missing_counts.replace(0, np.nan, inplace=True)
        missing_counts.dropna(axis=1, how='all', inplace=True)

        missing_counts_formatted = missing_counts.applymap(lambda x: f'{int(x)}' if pd.notnull(x) else '')
        missing_counts_formatted.reset_index(drop=False, inplace=True)

        return JsonResponse(missing_counts_formatted.to_dict('records'), safe=False)
    
@csrf_exempt
def generate_cal_plots(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        df = pd.DataFrame(data)
        calibrator_names = ['Калибратор 1', 'Калибратор 2', 'Калибратор 3', 'Калибратор 4', 'Калибратор 5', 'Калибратор 6']
        df = df[df['group'] == 'Cal']
        data_ref = pd.read_excel(ref_qc_data_file, sheet_name='References')
        metabolite_value = df['metabolite'].iloc[0]  # Get the metabolite value from the first row
        for i in range(6):
            fig, ax = plt.subplots(figsize=(6, 3))
            lower_limit = data_ref.loc[i, metabolite_value] * 0.80
            upper_limit = data_ref.loc[i, metabolite_value] * 1.2
            ax.axhline(y=lower_limit, color='blue', linestyle='--')
            ax.axhline(y=upper_limit, color='red', linestyle='--')
            color_1 = ''
            if df.loc[i, 'concentration'] >= upper_limit:
                color_1 = '#f57640'  # high-color
            elif df.loc[i, 'concentration'] <= lower_limit:
                color_1 = '#14b1ff'  # low-color
            else:
                color_1 = '#41b883b7'  # passed-color
            ax.plot(0.5, df.loc[i, 'concentration'], 'o', markersize=12, markerfacecolor=color_1, markeredgecolor=color_1, label=f'{calibrator_names[i]} ({df.loc[i, "concentration"]:.3f})', clip_on=False)
            ax.set_title(f'{calibrator_names[i]}')
            ax.set_ylim(lower_limit * 0.01, upper_limit * 1.8)
            ax.fill_betweenx([lower_limit * 0.01, lower_limit], 0, 1, color='deepskyblue', alpha=0.1)
            ax.fill_betweenx([lower_limit, upper_limit], 0, 1, color='springgreen', alpha=0.1)
            ax.fill_betweenx([upper_limit, upper_limit * 1.8], 0, 1, color='red', alpha=0.1)
            ax.set_xlim(0, 1)
            ax.legend(loc='upper right', markerscale=0)
            plt.tight_layout()
            plt.savefig(os.path.join(os.getcwd(), f'plot_{i+1}.png'), dpi=300)
            plt.close()

        return HttpResponse("Plots generated successfully!")
    
@csrf_exempt
def generate_cal_intra_projects_plots(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        df = pd.DataFrame(data)
        data_ref = pd.read_excel(ref_qc_data_file, sheet_name='References')
        calibrator_names = df[df['group'] == 'Cal']['sample'].unique()
        try:
            metabolite_value = df['metabolite'].iloc[0]
        except IndexError:
            metabolite_value = None
        
        for j, calibrator in enumerate(calibrator_names):
            cal_df = df[(df['group'] == 'Cal') & (df['sample'] == calibrator)]
            batches_nums = cal_df[['batch']].drop_duplicates()
            num_projects = len(batches_nums.values)

            fig, ax = plt.subplots(figsize=(6, 3))
            lower_limit = data_ref.loc[j, metabolite_value] * 0.80
            upper_limit = data_ref.loc[j, metabolite_value] * 1.20

            for i, num in enumerate(batches_nums['batch'].values):
                concentration = cal_df[(cal_df['batch'] == num) & (cal_df['metabolite'] == metabolite_value)]['concentration'].iloc[0]
                

                if concentration >= upper_limit:
                    color_1 = '#f57640'  # high-color
                elif concentration < lower_limit:
                    color_1 = '#14b1ff'  # low-color
                else:
                    color_1 = '#41b883b7'  # passed-color
                    
                ax.axline((i-0.5, 0), (i-0.5, concentration), color='gray', linestyle='--', alpha=0.5)
                if i == len(batches_nums) - 1:
                    ax.axline((i+0.5, 0), (i+0.5, concentration), color='gray',  linestyle='--', alpha=0.5)

                ax.plot(range(len(batches_nums)), [cal_df[cal_df['batch'] == num]['concentration'].iloc[0] for num in batches_nums['batch'].values], linestyle='--', color='gray', alpha=0.5, linewidth=0.6)
                ax.plot(i, concentration, 'o', markersize=12, label=f'Batch {num}', color=color_1)

            ax.set_xticks(range(len(batches_nums)))
            ax.set_xticklabels([f'Batch {num}' for num in batches_nums.values], rotation=30, ha='right')
            ax.axhline(y=lower_limit, color='blue', linestyle='--')
            ax.axhline(y=upper_limit, color='red', linestyle='--')
            ax.set_ylim(lower_limit * 0.01, upper_limit * 1.8)
            ax.set_xlim(-1, num_projects)
            ax.fill_betweenx([lower_limit * 0.01, lower_limit], -1, num_projects, color='deepskyblue', alpha=0.1)
            ax.fill_betweenx([lower_limit, upper_limit], -1, num_projects, color='springgreen', alpha=0.1)
            ax.fill_betweenx([upper_limit, upper_limit * 1.8], -1, num_projects, color='red', alpha=0.1)

            ax.set_title(f'{calibrator}')
            ax.set_ylabel('Concentration')
            # ax.set_xlabel('Batch')

            plt.tight_layout()
            plt.savefig(os.path.join(os.getcwd(), f'plot_{j+1}.png'), dpi=300)
            plt.close()

        return HttpResponse("Plots generated successfully!")
    
@csrf_exempt
def get_cal_intra_projects_plot(request, plot_number):
    image_path = os.path.join(os.getcwd(), f'plot_{plot_number}.png')
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return HttpResponse(image_data, content_type='image/png')
    
@csrf_exempt
def get_cal_plot(request, plot_number):
    image_path = os.path.join(os.getcwd(), f'plot_{plot_number}.png')
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return HttpResponse(image_data, content_type='image/png')

@csrf_exempt
def generate_qc_plots(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        df = pd.DataFrame(data)
        df = df[df['group'] == 'QC']
        data_ref = pd.read_excel(ref_qc_data_file, sheet_name='References')
        metabolite = df['metabolite'].iloc[0]  # Get the metabolite value from the first row

        # row contain LQC, MQC, HQC
        QCs = [df[df['sample'].str.contains('LQC')], df[df['sample'].str.contains('MQC')], df[df['sample'].str.contains('HQC')]]

        for i, qc in enumerate(QCs):
            fig, axs = plt.subplots(1, 1, figsize=(6, 3))  # Create a new figure for each plot

            value_1 = qc['concentration'].iloc[0]
            value_2 = qc['concentration'].iloc[1]
            lower_limit = data_ref.loc[i + 6, metabolite] * 0.85  # Нижняя граница
            upper_limit = data_ref.loc[i + 6, metabolite] * 1.15  # Верхняя граница
            
            axs.set_title(qc['sample'].iloc[0][:-2])
            
            # Отрисовка границ
            axs.axhline(y=lower_limit, color='blue', linestyle='--', label='Нижняя граница')
            axs.axhline(y=upper_limit, color='red', linestyle='--', label='Верхняя граница')

            # Определение цвета для точек
            color_1 = ''
            color_2 = ''
            if value_1 >= upper_limit:
                color_1 = '#f57640'  # high-color
            elif value_1 <= lower_limit:
                color_1 = '#14b1ff'  # low-color
            else:
                color_1 = '#41b883b7'  # passed-color

            if value_2 >= upper_limit:
                color_2 = '#f57640'  # high-color
            elif value_2 <= lower_limit:
                color_2 = '#14b1ff'  # low-color
            else:
                color_2 = '#41b883b7'  # passed-color

            # Отрисовка точек
            axs.plot(0.25, value_1, 'o', markersize=10, color=color_1, label='QC 1')  # 'o' - круг
            axs.plot(0.75, value_2, 'o', markersize=10, color=color_2, label='QC 2')  # 'o' - круг

            # Закрашивание области между границами
            axs.fill_betweenx([lower_limit, upper_limit], 0, 1, color='springgreen', alpha=0.1)
            axs.fill_betweenx([0, lower_limit], 0, 1, color='deepskyblue', alpha=0.1)
            axs.fill_betweenx([upper_limit, upper_limit / 0.8], 0, 1, color='red', alpha=0.1)

            # Настройка заголовка и меток
            axs.legend([f'QC 1 ({value_1:.3f})', f'QC 2 ({value_2:.3f})'], loc='upper right', handlelength=0, handletextpad=0)
            axs.set_ylabel('Значение')
            axs.set_ylim(lower_limit * 0.5, upper_limit / 0.8)
            axs.set_xlim(0, 1)
            

            plt.savefig(os.path.join(os.getcwd(), f'plot_qc_{i+1}.png'), bbox_inches='tight', dpi=300)
            plt.close()

        return HttpResponse("Plots generated successfully!")
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_qc_plot(request, plot_number):
    image_path = os.path.join(os.getcwd(), f'plot_qc_{plot_number}.png')
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return HttpResponse(image_data, content_type='image/png')


@csrf_exempt
def generate_intra_qc_plots(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        df = pd.DataFrame(data)
        df = df[df['group'] == 'QC']
        data_ref = pd.read_excel(ref_qc_data_file, sheet_name='References')
        
        try:
            metabolite = df['metabolite'].iloc[0]
        except IndexError:
            metabolite = None

        # row contain LQC, MQC, HQC
        QCs = [df[df['sample'].str.contains('LQC')], df[df['sample'].str.contains('MQC')], df[df['sample'].str.contains('HQC')]]

        for i, qc in enumerate(QCs):
            batches_nums = qc[['batch']].drop_duplicates()
            num_projects = len(batches_nums.values)

            fig, ax = plt.subplots(figsize=(6, 3))
            lower_limit = data_ref.loc[i + 6, metabolite] * 0.85  # Нижняя граница
            upper_limit = data_ref.loc[i + 6, metabolite] * 1.15  # Верхняя граница

            for j, num in enumerate(batches_nums['batch'].values):
                qc1 = qc[(qc['batch'] == num) & (qc['sample'].str.contains('-1'))]
                qc2 = qc[(qc['batch'] == num) & (qc['sample'].str.contains('-2'))]

                value_1 = qc1['concentration'].iloc[0]
                value_2 = qc2['concentration'].iloc[0]

                color_1 = ''
                color_2 = ''
                if value_1 >= upper_limit:
                    color_1 = '#f57640'  # high-color
                elif value_1 <= lower_limit:
                    color_1 = '#14b1ff'  # low-color
                else:
                    color_1 = '#41b883b7'  # passed-color

                if value_2 >= upper_limit:
                    color_2 = '#f57640'  # high-color
                elif value_2 <= lower_limit:
                    color_2 = '#14b1ff'  # low-color
                else:
                    color_2 = '#41b883b7'  # passed-color

                ax.plot(j-0.2, value_1, 'o', markersize=10, color=color_1, label=f'Batch {num}-1')
                ax.plot(j+0.2, value_2, 'o', markersize=10, color=color_2, label=f'Batch {num}-2')

                ax.axhline(y=lower_limit, color='blue', linestyle='--')
                ax.axhline(y=upper_limit, color='red', linestyle='--')

                ax.axline((j-0.5, 0), (j-0.5, max(value_1, value_2)), color='gray', linestyle='--', alpha=0.5)
                if j == len(batches_nums) - 1:
                    ax.axline((j+0.5, 0), (j+0.5, max(value_1, value_2)), color='gray', linestyle='--',  alpha=0.5)

            ax.set_xticks(range(len(batches_nums)))
            ax.set_xticklabels([f'Batch {num}' for num in batches_nums.values], rotation=30, ha='center')
            ax.set_ylim(lower_limit * 0.5, upper_limit / 0.8)
            ax.set_xlim(-1, num_projects)
            ax.fill_betweenx([lower_limit, upper_limit], -1, num_projects, color='springgreen', alpha=0.1)
            ax.fill_betweenx([0, lower_limit], -1, num_projects, color='deepskyblue', alpha=0.1)
            ax.fill_betweenx([upper_limit, upper_limit / 0.8], -1, num_projects, color='red', alpha=0.1)

            ax.set_title(qc['sample'].iloc[0][:-2])
            ax.set_ylabel(f'Concentration')

            plt.tight_layout()
            plt.savefig(os.path.join(os.getcwd(), f'plot_qc_{i+1}.png'), dpi=300)
            plt.close()

        return HttpResponse("Plots generated successfully!")
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_intra_qc_plots(request, plot_number):
    image_path = os.path.join(os.getcwd(), f'plot_qc_{plot_number}.png')
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return HttpResponse(image_data, content_type='image/png')
        

@csrf_exempt
def generate_labqc_plots(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        df = pd.DataFrame(data)
        df = df[df['group'] == 'labQC']
        metabolite = data[0]['metabolite']
        data_ref = pd.read_excel(ref_qc_data_file, sheet_name='References')

        low_limit = data_ref.loc[10, metabolite] # Нижняя граница
        Very_low_limit = data_ref.loc[11, metabolite] # Нижняя граница
        up_limit = data_ref.loc[12, metabolite] # Верхняя граница
        Very_up_limit = data_ref.loc[13, metabolite] # Верхняя граница

        concentrations = df[df['metabolite'] == metabolite]['concentration'].values

        colors = []
        for value in concentrations:
            if low_limit < value < up_limit:
                colors.append('#41b883b7')
            elif Very_low_limit < value <= low_limit:
                colors.append('#14b1ff')
            elif up_limit <= value < Very_up_limit:
                colors.append('#f57640')
            elif Very_up_limit <= value:
                colors.append('#f57640')
            else:
                colors.append('#14b1ff')

        plt.figure(figsize=(8, 4))

        plt.fill_betweenx([Very_low_limit*0.8, Very_low_limit], 0, len(concentrations)+1, color='lightskyblue', alpha=0.3)
        plt.fill_betweenx([low_limit, up_limit], 0, len(concentrations)+1, color='springgreen', alpha=0.1)
        plt.fill_betweenx([up_limit, Very_up_limit], 0, len(concentrations)+1, color='salmon', alpha=0.1)
        plt.fill_betweenx([Very_low_limit, low_limit], 0, len(concentrations)+1, color='lightskyblue', alpha=0.2)
        plt.fill_betweenx([Very_up_limit, Very_up_limit*1.2], 0, len(concentrations)+1, color='red', alpha=0.1)

        plt.axhline(y=low_limit, color='steelblue', linestyle='--')
        plt.axhline(y=up_limit, color='lightsalmon', linestyle='--')
        plt.axhline(y=Very_low_limit, color='blue', linestyle='--')
        plt.axhline(y=Very_up_limit, color='red', linestyle='--')

        plt.xlim(0, len(concentrations) +1)

        plt.ylim(Very_low_limit*0.8, Very_up_limit*1.2)
        plt.scatter(range(1, len(concentrations)+1), concentrations, color=colors, s=100)

        plt.savefig(os.path.join(os.getcwd(), f'plot_labqc.png'), bbox_inches='tight', dpi=300)
        plt.close()

        return HttpResponse("Plots generated successfully!")
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def get_labqc_plot(response):
    image_path = os.path.join(os.getcwd(), f'plot_labqc.png')
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return HttpResponse(image_data, content_type='image/png')

@csrf_exempt
def generate_intra_labqc_plots(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        df = pd.DataFrame(data)
        df = df[df['group'] == 'labQC']
        metabolite = data[0]['metabolite']
        data_ref = pd.read_excel(ref_qc_data_file, sheet_name='References')

        low_limit = data_ref.loc[10, metabolite]  # Нижняя граница
        Very_low_limit = data_ref.loc[11, metabolite]  # Нижняя граница
        up_limit = data_ref.loc[12, metabolite]  # Верхняя граница
        Very_up_limit = data_ref.loc[13, metabolite]  # Верхняя граница

        concentrations = df[df['metabolite'] == metabolite]['concentration'].values

        colors = []
        for value in concentrations:
            if low_limit < value < up_limit:
                colors.append('#41b883b7')
            elif Very_low_limit < value <= low_limit:
                colors.append('#14b1ff')
            elif up_limit <= value < Very_up_limit:
                colors.append('#f57640')
            elif Very_up_limit <= value:
                colors.append('#f57640')
            else:
                colors.append('#14b1ff')

        plt.figure(figsize=(8, 4))

        plt.fill_betweenx([Very_low_limit*0.8, Very_low_limit], -1, len(concentrations)+1, color='lightskyblue', alpha=0.3)
        plt.fill_betweenx([low_limit, up_limit], -1, len(concentrations)+1, color='springgreen', alpha=0.1)
        plt.fill_betweenx([up_limit, Very_up_limit], -1, len(concentrations)+1, color='salmon', alpha=0.1)
        plt.fill_betweenx([Very_low_limit, low_limit], -1, len(concentrations)+1, color='lightskyblue', alpha=0.2)
        plt.fill_betweenx([Very_up_limit, Very_up_limit*1.2], -1, len(concentrations)+1, color='red', alpha=0.1)

        plt.axhline(y=low_limit, color='steelblue', linestyle='--')
        plt.axhline(y=up_limit, color='lightsalmon', linestyle='--')
        plt.axhline(y=Very_low_limit, color='blue', linestyle='--')
        plt.axhline(y=Very_up_limit, color='red', linestyle='--')

        plt.xlim(-1, len(concentrations) +1)

        plt.ylim(Very_low_limit*0.8, Very_up_limit*1.2)

        batch_nums = df['batch'].unique()
        xtick_labels = []
        xtick_positions = []
        concentrations_all = []
        colors_all = []
        for j, num in enumerate(batch_nums):
            batch_df = df[df['batch'] == num]
            concentrations_batch = batch_df['concentration'].values
            colors_batch = [color for concentration, color in zip(concentrations, colors) if concentration in concentrations_batch]
            concentrations_all.extend(concentrations_batch)
            colors_all.extend(colors_batch)

        # Add gap between batches
        x_values = []
        for i, concentration in enumerate(concentrations_all):
            if i == 0:
                x_values.append(i)
            else:
                x_values.append(i + 0.5)  # Add 0.5 gap between batches

        plt.scatter(x_values, concentrations_all, color=colors_all, s=100)

        last_point = 0
        for j, num in enumerate(batch_nums):
            batch_df = df[df['batch'] == num]
            concentrations_batch = batch_df['concentration'].values
            if j < len(batch_nums) - 1:
                plt.axvline(x=last_point + len(concentrations_batch), color='gray', linestyle='--', alpha=0.5)
            last_point += len(concentrations_batch) 

            xtick_labels.append(f'Batch {num}')
            xtick_positions.append(last_point - len(concentrations_batch) / 2 - 0.25)  # Adjust xtick position

        plt.xticks(xtick_positions, xtick_labels, rotation=30, ha='center')

        # Add gap from left corner and right corner of plot
        plt.xlim(-1, len(concentrations_all) + 1)

        plt.savefig(os.path.join(os.getcwd(), f'plot_intra_labqc.png'), bbox_inches='tight', dpi = 300)
        plt.close()

        return HttpResponse("Plots generated successfully!")
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def get_intra_labqc_plot(response):
    image_path = os.path.join(os.getcwd(), f'plot_intra_labqc.png')
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return HttpResponse(image_data, content_type='image/png')
