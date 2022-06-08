#!usr/bin/env python3



#General Main Bot Stats Area
gen_bot_main_stats_query=  '''INSERT INTO ln_genBotsMainStats(id,project_id,botName,botStats,botStatsProp,isNumeric,month,year,notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
gen_bot_main_by_target_query =  '''INSERT INTO ln_genBotsMainStatsByTarget(id,target, value, valueProp, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
gen_bot_main_by_source_query = '''INSERT INTO ln_genBotsMainStatsBySource(id, source, value, valueProp, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
gen_bot_main_by_method_query = '''INSERT INTO ln_genBotsMainStatsByMethod(id, method, value, valueProp, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
gen_bot_main_by_verification = '''INSERT INTO ln_genBotsMainStatsByVerification(id, verified, unverified, month, year, project_id) VALUES (%s, %s, %s, %s, %s, %s) '''
gen_bot_main_by_ref_page_query = '''INSERT INTO ln_genBotsMainStatsByRefPage(id, url, value, valueProp, month, year, project_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'''

#Goolge Bot Stats Area
google_bot_main_by_source_query = '''INSERT INTO ln_googleBotMainStatsBySource(id, source, value, valueProp, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
google_bot_main_by_target_query = '''INSERT INTO ln_googleBotsMainStatsByTarget(id, source, value, valueProp, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''

#Google Bot Stats Area - Direct Hits
google_bot_direct_hit_main_query = '''INSERT INTO ln_googleBotsStatsDirectHit(id, url, value, valueProp, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
google_bot_direct_hit_by_stcode_query = '''INSERT INTO ln_googleBotsStatsDirectHitByStCode(id, status_code, value, valueProp, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
google_bot_direct_hit_by_page_query = '''INSERT INTO ln_googleBotsStatsDirectHitByBigPage(id, target, value, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''
google_bot_direct_hit_by_bigimage_query = '''INSERT INTO ln_googleBotsStatsDirectHitByBigImage(id, target, size,month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''
google_bot_direct_hit_by_bigcss_query = '''INSERT INTO ln_googleBotsStatsDirectHitByBigCSS(id, target, size,month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''
google_bot_direct_hit_by_bigjson_query = '''INSERT INTO ln_googleBotsStatsDirectHitByBigJson(id, target, size,month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''
google_bot_direct_hit_by_php_query = '''INSERT INTO ln_googleBotsStatsDirectHitByPhP(id, target, value, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''

#Google bot Stats Area - Non DIrect Hits
google_bot_ndirect_hit_main_query = '''INSERT INTO ln_googleBotsStatsNDHit(id, url, value, valueProp, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
google_bot_ndirect_hit_by_stcode_query = '''INSERT INTO ln_googleBotsStatsNDHitByCode(id, status_code, value, valueProp, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
google_bot_ndirect_hit_by_bigimage_query = '''INSERT INTO ln_googleBotsStatsNDirectHitByBigImage(id, target, size,month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''
google_bot_ndirect_hit_by_bigcss_query = '''INSERT INTO ln_googleBotsStatsNDirectHitByBigCSS(id, target, size,month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''
google_bot_ndirect_hit_by_bigjson_query = '''INSERT INTO ln_googleBotsStatsNDirectHitByBigJson(id, target, size,month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''
google_bot_ndirect_hit_by_page_query = '''INSERT INTO ln_googleBotsStatsNDirectHitByBigPage(id, target, size, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''
google_bot_ndirect_hit_by_php_query = '''INSERT INTO ln_googleBotsStatsNDirectHitByPhP(id, target, size, month, year, project_id) VALUES (%s,%s,%s,%s,%s,%s)'''
