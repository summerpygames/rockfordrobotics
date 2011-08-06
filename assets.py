import os
assets = 'data'
button = 'button'
allign = 'allign'
message = 'message'
sounds = 'sounds'

##########################
## To complete this file##
##  REPLACE the '.svg'  ##
##########################
# EDIT THIS IN NOTEPAD++ #
##########################

###########################################
##  For the Main Menu                    ##
###########################################

main_allign = os.path.join(assets, allign, 'main.svg')
main_play_des = os.path.join(assets, button, 'mmplay.svg')
main_howto_des = os.path.join(assets, button, 'mmhtp.svg')
main_credits_des = os.path.join(assets, button, 'mmcredits.svg')
main_about_des = os.path.join(assets, button, 'mmabout.svg')
main_play_sel = os.path.join(assets, button, 'mmplayselect.svg')
main_howto_sel = os.path.join(assets, button, 'mmhtpselected.svg')
main_credits_sel = os.path.join(assets, button, 'mmcreditsselect.svg')
main_about_sel = os.path.join(assets, button, 'mmaboutselect.svg')

###########################################
##  For the Grades menu                  ##
###########################################

grades_allign = os.path.join(assets, allign, 'gmalign.svg')
grades_resume_des = os.path.join(assets, button, 'gmresume.svg')
grades_1_des = os.path.join(assets, button, 'gm1st.svg')
grades_2_des = os.path.join(assets, button, 'gm2nd.svg')
grades_3_des = os.path.join(assets, button, 'gm3rd.svg')
grades_resume_sel = os.path.join(assets, button, 'gmresumeselect.svg')
grades_1_sel = os.path.join(assets, button, 'gm1stselect.svg')
grades_2_sel = os.path.join(assets, button, 'gm2ndselect.svg')
grades_3_sel = os.path.join(assets, button, 'gm3rdselect.svg')

###########################################
##  For the How to Play menu             ##
###########################################

htpl_allign = os.path.join(assets, allign, 'howtoplay.svg')

###########################################
##  For the Charecter Selection Menu     ##
###########################################

charecter_allign = os.path.join(assets, allign, 'chalign.svg')
charecter_wilber_des = os.path.join(assets, button, 'chgimp.svg')
charecter_tux_des = os.path.join(assets, button, 'chtux.svg')
charecter_python_des = os.path.join(assets, button, 'chpython.svg')
charecter_gnu_des = os.path.join(assets, button, 'chgnu.svg')
charecter_wilber_sel = os.path.join(assets, button, 'chgimpselect.svg')
charecter_tux_sel = os.path.join(assets, button, 'chtuxselect.svg')
charecter_python_sel = os.path.join(assets, button, 'chpythonselect.svg')
charecter_gnu_sel = os.path.join(assets, button, 'chgnuselect.svg')

###########################################
##  For the Stage Selection Menu         ##
###########################################

stage_allign = os.path.join(assets, allign, 'stalign.svg')
stage_deep_des = os.path.join(assets, button, 'stdeepstage.svg')
stage_solar_des = os.path.join(assets, button, 'stsolar.svg')
stage_planet_des = os.path.join(assets, button, 'stbarren.svg')
stage_city_des = os.path.join(assets, button, 'sthome.svg')
stage_locked_des = os.path.join(assets, button, 'stlocked.svg')
stage_deep_sel = os.path.join(assets, button, 'stdeepstageselect.svg')
stage_solar_sel = os.path.join(assets, button, 'stsolarselect.svg')
stage_planet_sel = os.path.join(assets, button, 'stbarrenselect.svg')
stage_city_sel = os.path.join(assets, button, 'sthomeselect.svg')
stage_locked_sel = os.path.join(assets, button, 'stlockedselect.svg')

###########################################
##  For the Level Selection Menu         ##
###########################################

level_allign = os.path.join(assets, allign, 'lmalign.svg')
level_math_des = os.path.join(assets, button, 'lmallmath.svg')
level_played_des = os.path.join(assets, button, 'lmplayed.svg')
level_unlock_des = os.path.join(assets, button, 'lmunlocked.svg')
level_lock_des = os.path.join(assets, button, 'lmlocked.svg')
level_math_sel = os.path.join(assets, button, 'lmallmathselect.svg')
level_played_sel = os.path.join(assets, button, 'lmplayedselect.svg')
level_unlock_sel = os.path.join(assets, button, 'lmunlockedselect.svg')
level_lock_sel = os.path.join(assets, button, 'lmlockedselect.svg')


###########################################
##  For the About the Team Menu          ##
###########################################

about_allign = os.path.join(assets, allign, 'aboutmenu.svg')

###########################################
##  For the Credits Menu                 ##
###########################################

credits_allign = os.path.join(assets, allign, 'creditsmenu.svg')

###########################################
## Databases                             ##
###########################################

gameplay_database = os.path.join(assets, 'gamedatabase.db')

###########################################
## Lifes                                 ##
###########################################
life_full = os.path.join(assets, 'wholeheart.svg')
life_empty = os.path.join(assets, 'brokenheart.svg')

question_box = os.path.join(assets, button, 'questionbox.svg')

###########################################
## OSD Messages                          ##
###########################################
great_job = os.path.join(assets, message, 'greatjob.svg')
incorrect = os.path.join(assets, message, 'incorrect.svg')
correct = os.path.join(assets, message, 'correct.svg')
ouch = os.path.join(assets, message, 'ouch.svg')

###########################################
## Sounds                                ##
###########################################
laser1 = os.path.join(assets, sounds, 'highlaser.ogg')
laser2 = os.path.join(assets, sounds, 'midlaser.ogg')
laser3 = os.path.join(assets, sounds, 'lowlaser.ogg')

sound_correct = os.path.join(assets, sounds, 'correct.ogg')
sound_gameover = os.path.join(assets, sounds, 'gameover.ogg')
sound_homeworld = os.path.join(assets, sounds, 'homeworld.ogg')
sound_lifeless = os.path.join(assets, sounds, 'life-1.ogg')
sound_mainmenu = os.path.join(assets, sounds, 'mainmenu.ogg')
sound_planet = os.path.join(assets, sounds, 'planet.ogg')
sound_solarsystem = os.path.join(assets, sounds, 'solarsystem.ogg')
sound_space = os.path.join(assets, sounds, 'space.ogg')



###########################################
## Charecters                            ##
###########################################
charecter_flying_saucer = os.path.join(assets, 'pythonsaucer.svg')
charecter_space_shuttle = os.path.join(assets, 'tuxshuttle.svg')
charecter_classic_rocket = os.path.join(assets, 'gnurocket.svg')
charecter_fighter_jet = os.path.join(assets, 'gimpfighter.svg')

###########################################
## Backgrounds                           ##
###########################################
background_deepspace = os.path.join(assets, 'spacebg.jpg')
background_solarsystem = os.path.join(assets, 'solarsystem.jpg')
background_barrenplanet = os.path.join(assets, 'barrenplanet.jpg')
background_homeworld = os.path.join(assets, 'homeworld.jpg')
