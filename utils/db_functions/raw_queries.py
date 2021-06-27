QUERY_FOR_REGISTER_DOCTOR = """INSERT INTO doctors VALUES (nextval('doctors_id_seq'),:username,:full_name,:mail,:password,
            :phone_number,:gender,:experience,:econsultation_fee,:is_active,:is_online,:url,:follow_up_fee,:about, 
            :slug, :created_on) RETURNING id """

QUERY_FOR_SAVE_SPECIALISATION = """INSERT INTO specialisations VALUES (nextval('specialisations_id_seq'),:name,:is_active,now() at time zone 'UTC') """

QUERY_FOR_SAVE_LANGUAGE = "INSERT INTO doctors_languages_map VALUES (nextval('doctors_languages_map_id_seq'),:doctor_id,:languages_id,now() at time zone 'UTC') "

QUERY_FOR_SAVE_QUALIFICATION = "INSERT INTO qualifications VALUES (nextval('qualifications_id_seq'),:doctor_id,:qualification_name," \
                               ":institute_name,:year) "

QUERY_FOR_FIND_ALL_LANGUAGES = "SELECT * FROM languages"

QUERY_FOR_GET_QUALIFICATIONS = "SELECT * FROM qualifications where doctor_id=:doctor_id"

QUERY_FOR_GET_SPECIFIC_QUALIFICATION_ID = "SELECT * FROM qualifications WHERE id=:id"

WHERE_ID_QUALIFICATIONS = " WHERE id=:id"

QUERY_FOR_SPECIFIC_DOCTOR_LANGUAGE = "SELECT doctors_languages_map.doctor_id, doctors_languages_map.created_on, " \
                                     "languages.name,languages.is_active FROM doctors_languages_map INNER JOIN " \
                                     "languages ON doctors_languages_map.languages_id = languages.id WHERE " \
                                     "doctors_languages_map.doctor_id=:doctor_id "

WHERE_ID_DOCTORS = " WHERE id=:id RETURNING id"

QUERY_FOR_SPECIALISATION_MAP = "INSERT INTO doctors_specialisations_map VALUES (nextval('doctors_specialisations_map_id_seq'),:doctor_id,:specialisation_id) "

QUERY_FOR_UPDATE_DOCTORS_INFORMATION = "UPDATE doctors SET "

INSERT_QUERY_FOR_TIMESLOT = " INSERT INTO doctors_time_slot VALUES (nextval('doctors_time_slot_id_seq'),:day,:video,:audio,:chat,:start_time,:end_time,:video_frequency,:audio_frequency,:chat_frequency,:is_available,:non_availability_reason,:is_active,now() at time zone 'UTC') RETURNING id; "

QUERY_FOR_DOCTORS_QUALIFICATIONS_SELECT = "SELECT doctors.id,doctors.full_name,doctors.mail,doctors.gender,doctors.phone_number,doctors.experience,doctors.econsultation_fee,doctors.is_active,doctors.slug,doctors.url,doctors.about,doctors.is_online,qualifications.qualification_name,qualifications.institute_name,qualifications.year FROM doctors INNER JOIN qualifications ON doctors.id = qualifications.doctor_id"

QUERY_FOR_DOCTOR_SPECIALISATION_MAP = "SELECT doctors_specialisations_map.doctor_id,doctors_specialisations_map.specialisation_id,specialisations.name,specialisations.is_active FROM doctors_specialisations_map INNER JOIN specialisations ON doctors_specialisations_map.specialisation_id=specialisations.id WHERE doctor_id=:doctor_id"

QUERY_FOR_SPECIFIC_DOCTORS_DETAILS = """SELECT id,username,full_name,mail,phone_number,gender,experience,econsultation_fee,is_active,url,
        is_online,follow_up_fee,about,slug FROM doctors WHERE id=:id """

QUERY_FOR_FIND_FIRST_DOCTOR_SPECIALISATION = "SELECT specialisations.name FROM doctors_specialisations_map INNER JOIN specialisations ON doctors_specialisations_map.specialisation_id=specialisations.id WHERE doctor_id=:doctor_id ORDER BY specialisation_id LIMIT 1"

QUERY_FOR_UPDATE_SLUG = "UPDATE doctors SET slug=:slug WHERE id=:id"

QUERY_FOR_SAVE_TIMESLOT_CONFIG = " INSERT INTO doctors_time_slot VALUES (nextval('doctors_time_slot_id_seq'),:day,:video,:audio,:chat,:start_time,:end_time,:video_frequency,:audio_frequency,:chat_frequency,:is_available,:non_availability_reason,:is_active,now() at time zone 'UTC') RETURNING id; "

QUERY_FOR_DOCTOR_SCHEDULE = "SELECT day,start_time,end_time,doctor_id FROM doctors_time_slot INNER JOIN doctors_timeslot_map ON doctors_time_slot.id = doctors_timeslot_map.time_slot_id WHERE start_time<=now() at time zone 'UTC' AND doctor_id=:doctor_id"

QUERY_FOR_DOCTOR_EXIST_IN_TIMESLOT_CONFIG = "SELECT id FROM doctors_timeslot_map WHERE doctor_id=:doctor_id"

QUERY_FOR_DOCTOR_END_TIME = "SELECT id,patient_id,doctor_id FROM consultations WHERE doctor_id=:doctor_id AND " \
                            "time_slot_config_id=:time_slot_config_id AND end_time>=:end_time"

QUERY_FOR_DOCTOR_START_TIME = "SELECT id,patient_id,doctor_id FROM consultations WHERE doctor_id=:doctor_id AND " \
                              "time_slot_config_id=:time_slot_config_id AND start_time<=:start_time"

QUERY_FOR_FIND_TIME = "SELECT doctors_time_slot.id,doctors_time_slot.day,doctors_time_slot.video,doctors_time_slot.audio," \
                      "doctors_time_slot.chat,doctors_time_slot.start_time,doctors_time_slot.end_time," \
                      "doctors_time_slot.video_frequency,doctors_time_slot.audio_frequency," \
                      "doctors_time_slot.chat_frequency FROM doctors_time_slot INNER JOIN doctors_timeslot_map ON " \
                      "doctors_time_slot.id = doctors_timeslot_map.time_slot_id WHERE " \
                      "doctors_timeslot_map.doctor_id=:doctor_id AND doctors_time_slot.day=:day AND " \
                      "doctors_time_slot.start_time >= now() at time zone 'UTC' AND " \
                      "doctors_time_slot.is_available=True "

QUERY_FOR_FIND_BOOKED_SLOTS = """SELECT start_time,end_time,time_slot_config_id FROM consultations where doctor_id=:doctor_id AND day=:day AND start_time>=now() at time zone 'UTC' """

QUERY_FOR_ALL_DAYS_TIME = "SELECT doctors_time_slot.id,doctors_time_slot.day,doctors_time_slot.video," \
                          "doctors_time_slot.audio," \
                          "doctors_time_slot.chat,doctors_time_slot.start_time,doctors_time_slot.end_time," \
                          "doctors_time_slot.video_frequency,doctors_time_slot.audio_frequency," \
                          "doctors_time_slot.chat_frequency FROM doctors_time_slot INNER JOIN doctors_timeslot_map ON " \
                          "doctors_time_slot.id = doctors_timeslot_map.time_slot_id WHERE " \
                          "doctors_timeslot_map.doctor_id=:doctor_id AND " \
                          "doctors_time_slot.start_time >= now() at time zone 'UTC' AND " \
                          "doctors_time_slot.is_available=True "


QUERY_FOR_FIND_BOOKED_TIME_SLOTS_FOR_ALL_DAYS = """SELECT start_time,end_time,time_slot_config_id FROM consultations where doctor_id=:doctor_id AND start_time>=now() at time zone 'UTC' """