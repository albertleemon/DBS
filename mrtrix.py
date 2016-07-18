import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.interfaces.mrtrix as mrtrix  # <---- The important new part!
import nipype.interfaces.fsl as fsl
import nipype.algorithms.misc as misc
import os,sys,glob
import os.path as op                     # system functions
import subprocess
import numpy

# list1 = ['AA66',10.31,8.14,2.42,-15.29,6.62,0.65]
# list2 = ['HG60',14.97,17.06,-3.76,-10.63,15.67,-1.76]
# list3 = ['HG60_2',15.53,17.06,-3.39,-10.63,15.39,-2.39 ]
# list4 = ['HS61_65',14.42,9.55,-2.39,-9.79,8.71,-0.39]
# list5 = ['HS65_61',4.12,32.92,11.61,-18.97,29.3,7.61]
# list6 = ['KM64',12.75,7.04,2.84,-12.85,6.76,2.84]
# list7 = ['KM75',10.24,9.55,0.84,-12.29,9.27,0.84]
# list8 = ['KW46',18.59,14.84,-3.73,-3.67,15.67,-3.73]
# list9 = ['KW51',14.97,15.39,-11.73,-10.63,17.34,-11.73]
# list10 = ['MP65',13.03,21.79,-11.73,-8.67,21.51,-11.73]
# list11 = ['MR57',17.48,10.66,10.54,-7.28,10.1,12.54]
# list12 = ['OD62',11.64,26.52,-5.45,-11.18,24.57,-5.45]
# list13 = ['RU50',16.64,30.97,-38.93,-8.40,31.81,-42.93]
# list14 = ['RU50_2',15.25,31.53,-37.79,-9.23,32.09,-39.79]
# list15 = ['SA65',5.51,11.5,10.11,-16.19,14.28,10.11]
# list16 = ['SB40',12.47,4.54,-7.89,-15.08,4.82,-7.89]
# list17 = ['SE41',14.42,8.71,12.11,-10.63,8.71,10.11]
# list18 = ['SE51',8.30,6.48,0.11,-18.14,5.23,0.06]
# list19 = ['SR56',9.96,6.76,-7.94,-13.69,5.93,-7.94]
# list20 = ['TM60',26.94,18.17,-3.94,5.51,16.5,-3.942]
# list21 = ['WG54',14.42,22.9,6.06,-5.61,23.04,7.85]


subjids = ['AA66','BG49','HG60','HG60_2' ,'HS61_65','HS65_61','KM64','KM75','KW46','KW51','MP65','MR57','OD62','RU50','RU50_2','SA65','SB40','SE41','SE51','SR56','TM60','WG54']

LR_coordinates = numpy.matrix([[10.31,8.14,2.42,-15.29,6.62,0.65],
				[14.21,8.47,-9.633,-10,6.80,-7.66],
				[14.97,17.06,-3.76,-10.63,15.67,-1.76],
				[15.53,17.06,-3.39,-10.63,15.39,-2.39 ],
				[14.42,9.55,-2.39,-9.79,8.71,-0.39],
				[4.12,32.92,11.61,-18.97,29.3,7.61],
				[12.75,7.04,2.84,-12.85,6.76,2.84],
				[10.24,9.55,0.84,-12.29,9.27,0.84],
				[18.59,14.84,-3.73,-3.67,15.67,-3.73],
				[14.97,15.39,-11.73,-10.63,17.34,-11.73],
				[13.03,21.79,-11.73,-8.67,21.51,-11.73],
				[17.48,10.66,10.54,-7.28,10.1,12.54],
				[11.64,26.52,-5.45,-11.18,24.57,-5.45],
				[16.64,30.97,-38.93,-8.40,31.81,-42.93],
				[15.25,31.53,-37.79,-9.23,32.09,-39.79],
				[5.51,11.5,10.11,-16.19,14.28,10.11],
				[12.47,4.54,-7.89,-15.08,4.82,-7.89],
				[14.42,8.71,12.11,-10.63,8.71,10.11],
				[8.30,6.48,0.11,-18.14,5.23,0.06],
				[9.96,6.76,-7.94,-13.69,5.93,-7.94],
				[26.94,18.17,-3.94,5.51,16.5,-3.942],
				[14.42,22.9,6.06,-5.61,23.04,7.85]])


fsl.FSLCommand.set_default_output_type('NIFTI')

data_dir = '/media/meng/Data/DBS/Pakinson'
#subject_list = os.listdir(data_dir)
#subject_list.remove('PH59')
#subject_list.remove('BK53')
#subject_list.remove('SM79')
subject_list = ['BG49']
subject_list.sort()
# for subj in subject_list:
# 	data_subj = op.join(data_dir,subj)
# 	if op.isdir(data_subj): 
# 		mv_data = ('mv %s/*/* %s/' % (data_subj,data_subj))
# 		print mv_data
# 		os.system(mv_data)

for subj in subject_list:
	data_subj = op.join(data_dir,subj)
	if op.isdir(data_subj):
		os.chdir(data_subj)
 		dcm = ''
 		mrconvert = ''
 		print op.abspath(data_subj)
		print len(os.listdir(data_subj))
		if not op.exists('mrtrix'):
			os.mkdir('mrtrix')
			#print dcm
		niis = 	glob.glob(op.join(data_subj,'mrtrix','*.nii'))
	 	for dcm in os.listdir(data_subj):
		 	if len(niis) == 0:		 
		 		if 'mpr' in dcm.lower():
		 			mrconvert = ('mrconvert %s %s' % (op.join(data_subj,dcm),'mrtrix/T1.nii'))
		 		elif 'dico' in dcm.lower():
		 			mrconvert = ('mrconvert %s %s' % (op.join(data_subj,dcm),'mrtrix/dwi.mif'))
		 		elif 't2' in dcm.lower():
		 			mrconvert = ('mrconvert %s %s' % (op.join(data_subj,dcm),'mrtrix/T2.nii'))
		 		elif 'ct' in dcm.lower():
		 			mrconvert = ('mrconvert %s %s' % (op.join(data_subj,dcm),'mrtrix/CT.nii'))
		 		else:
		 			mrconvert = ''	 			
		 		print mrconvert
		 		os.system(mrconvert)


 		if op.isfile(op.join(data_subj,'mrtrix','dwi.mif')):
			dwipreproc = ('dwipreproc -rpe_none AP %s %s' %(op.join(data_subj,'mrtrix/dwi.mif'),op.join(data_subj,'mrtrix/dwi_preproc.mif')))
			if not op.isfile(op.join(data_subj,'mrtrix/dwi_preproc.mif')):
				os.system(dwipreproc)
			check_shells = ('mrinfo -shellcounts %s' % (op.join(data_subj,'mrtrix/dwi_preproc.mif')))
			print check_shells
			# os.system(check_shells)
			shellcounts = subprocess.Popen(check_shells,shell=True,stdout=subprocess.PIPE).communicate()[0].split(' ')
			print shellcounts
			create_b0 = ('mrconvert %s/dwi_preproc.mif -coord 3 0:%s - | mrmath -axis 3 - mean %s/dwi_mean_b0.nii' % (op.join(data_subj,'mrtrix'),int(shellcounts[0])-1,op.join(data_subj,'mrtrix'))) 	

			T22B0 = ('flirt -ref %s/dwi_mean_b0.nii -in %s/T2.nii -omat %s/T22B0.mat -out %s/T22B0.nii' % (op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix'))) 
			CT2T2 = ('flirt -ref %s/T22B0.nii -in %s/ct.nii -omat %s/CT2newT2.mat -out %s/CT2newT2.nii' % (op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix')))

			dwi2mask = ('dwi2mask %s/dwi_preproc.mif %s/dwi_mask.nii' % (op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix')))
			dwi_adc = ('dwi2tensor %s/dwi_preproc.mif -mask %s/dwi_mask.nii - | tensor2metric - -adc %s/dwi_adc.nii' % (op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix')))
			dwi_fa = ('dwi2tensor %s/dwi_preproc.mif -mask %s/dwi_mask.nii - | tensor2metric - -fa %s/dwi_fa.nii' % (op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix')))

			print create_b0
			print(T22B0)
			print(CT2T2)
			print(dwi2mask)
			print(dwi_adc)
			print(dwi_fa)
			os.system(create_b0)
			os.system(T22B0)
			os.system(CT2T2)
			os.system(dwi2mask)
			os.system(dwi_adc)
			os.system(dwi_fa)

			if op.isfile(op.join(data_subj,'mrtrix','CT2newT2.nii')) and not op.isfile(op.join(data_subj,'mrtrix','b_CT2newT2.nii')):
				ct_binary = ('fslmaths %s -thr 150 %s' %(op.join(data_subj,'mrtrix','CT2newT2.nii'), op.join(data_subj,'mrtrix','b_CT2newT2.nii')))
				print ct_binary
				os.system(ct_binary)


			if subj in subjids and len(glob.glob(op.join(data_subj,'mrtrix','*tck'))==0):
				print subj
				print subjids.index(subj)
				Lxyz = LR_coordinates[subjids.index(subj),0:3]	
				Rxyz = LR_coordinates[subjids.index(subj),3:6]	
				tckgen = ('tckgen -algorithm Tensor_Prob  %s/dwi_preproc.mif %s/Tensor_prob_L6.tck -seed_sphere %s,%s,%s,6 -maxlength 300 -number 100k;tckgen -algorithm Tensor_Prob  %s/dwi_preproc.mif %s/Tensor_prob_R6.tck -seed_sphere %s,%s,%s,6 -maxlength 300 -number 100k' % (op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix'),Lxyz[0,0],Lxyz[0,1],Lxyz[0,2],op.join(data_subj,'mrtrix'),op.join(data_subj,'mrtrix'),Rxyz[0,0],Rxyz[0,1],Rxyz[0,2])) 
				print tckgen
				os.system(tckgen)


































# infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']), name="infosource")
# infosource.iterables = ('subject_id', subject_list)

# info = dict(dwi=[['subject_id', 'data']],
#             bvecs=[['subject_id', 'bvecs']],
#             bvals=[['subject_id', 'bvals']])


# datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
#                                                outfields=list(info.keys())),
#                      name='datasource')

# datasource.inputs.template = "%s/%s"
# datasource.inputs.base_directory = data_dir
# datasource.inputs.field_template = dict(dwi='%s/%s.nii.gz')
# datasource.inputs.template_args = info
# datasource.inputs.sort_filelist = True
# inputnode = pe.Node(interface=util.IdentityInterface(fields=["dwi", "bvecs", "bvals"]), name="inputnode")

# dwipreproc = pe.Node(interface=mrtrix.dwipreproc(), name='dwipreproc')

# gunzip = pe.Node(interface=misc.Gunzip(), name='gunzip')
# dwi2tensor = pe.Node(interface=mrtrix.DWI2Tensor(), name='dwi2tensor')
# tensor2vector = pe.Node(interface=mrtrix.Tensor2Vector(), name='tensor2vector')
# tensor2adc = pe.Node(interface=mrtrix.Tensor2ApparentDiffusion(), name='tensor2adc')
# tensor2fa = pe.Node(interface=mrtrix.Tensor2FractionalAnisotropy(), name='tensor2fa')

# MRconvert = pe.Node(interface=mrtrix.MRConvert(), name='MRconvert')
# MRconvert.inputs.extract_at_axis = 3
# MRconvert.inputs.extract_at_coordinate = [0]
# threshold_b0 = pe.Node(interface=mrtrix.Threshold(), name='threshold_b0')
# median3d = pe.Node(interface=mrtrix.MedianFilter3D(), name='median3d')

# erode_mask_firstpass = pe.Node(interface=mrtrix.Erode(), name='erode_mask_firstpass')
# erode_mask_secondpass = pe.Node(interface=mrtrix.Erode(), name='erode_mask_secondpass')
# MRmultiply = pe.Node(interface=mrtrix.MRMultiply(), name='MRmultiply')
# MRmult_merge = pe.Node(interface=util.Merge(2), name="MRmultiply_merge")
# threshold_FA = pe.Node(interface=mrtrix.Threshold(), name='threshold_FA')
# threshold_FA.inputs.absolute_threshold_value = 0.7

# bet = pe.Node(interface=fsl.BET(mask=True), name='bet_b0')
# gen_WM_mask = pe.Node(interface=mrtrix.GenerateWhiteMatterMask(), name='gen_WM_mask')
# threshold_wmmask = pe.Node(interface=mrtrix.Threshold(), name='threshold_wmmask')
# threshold_wmmask.inputs.absolute_threshold_value = 0.4
