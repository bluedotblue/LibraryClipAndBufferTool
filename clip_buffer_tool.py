import arcpy

in_features_point = arcpy.GetParameterAsText(0)
in_radius = float(arcpy.GetParameterAsText(1))
in_features_polygon = arcpy.GetParameterAsText(2)
in_field_join_features = arcpy.GetParameterAsText(3)
in_field_oldarea = arcpy.GetParameterAsText(4)
in_table_population = arcpy.GetParameterAsText(5)
in_field_join_table = arcpy.GetParameterAsText(6)
in_field_pop = arcpy.GetParameterAsText(7)
out_features_clipbuffer = arcpy.GetParameterAsText(8)

arcpy.AddMessage('''Here are the specified -
+ Parameter 1: {0}
+ Radius: {1}
+ Parameter 2: {2}
+ Parameter 3: {3}
+ Parameter 4: {4}
+ Parameter 5: {5}
+ Parameter 6: {6}
+ Parameter 7: {7}
+ Output: {8}'''\
                 .format(in_features_point, in_radius, in_features_polygon, \
                         in_field_join_features, in_field_oldarea, in_table_population, \
                         in_field_join_table, in_field_pop, out_features_clipbuffer))

arcpy.AddMessage('''Environments -
+ Workspace: {0}
+ Overwrite: {1}
+ Scratch GDB: {2}
+ Package workspace: {3}'''\
    .format(arcpy.env.workspace, arcpy.env.overwriteOutput, \
        arcpy.env.scratchGDB, arcpy.env.packageWorkspace))

out_features_buffer = arcpy.env.scratchGDB + '\\lib_buffer'
buffer_distance = '{0} Miles'.format(in_radius)
arcpy.Buffer_analysis(in_features_point, out_features_buffer, buffer_distance)
arcpy.Clip_analysis(in_features_polygon, out_features_buffer, out_features_clipbuffer)

#Join population with clipped and buffered area and compute percent market share
arcpy.JoinField_management(out_features_clipbuffer, in_field_join_features, \
                           in_table_population, in_field_join_table, [in_field_pop])

cursor = arcpy.da.SearchCursor(out_features_clipbuffer, \
                               [in_field_oldarea, 'SHAPE@AREA', in_field_pop])
total_service = 0
for row in cursor:
    pop = row[1]/row[0]*row[2]
    total_service += pop

cursor = arcpy.da.SearchCursor(in_table_population, [in_field_pop])
total_pop = 0
cursor.reset()
for row in cursor:
    total_pop += row[0]

arcpy.AddMessage('Total population served: {}'.format(int(total_service)))
arcpy.AddMessage('Percent of service: {}'.format(int(100*total_service/total_pop)))
