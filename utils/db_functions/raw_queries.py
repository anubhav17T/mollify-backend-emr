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

QUERY_FOR_SPECIFIC_DOCTOR_LANGUAGE = "SELECT doctors_languages_map.doctor_id, doctors_languages_map.created_on, languages.name,languages.is_active FROM doctors_languages_map INNER JOIN languages ON doctors_languages_map.languages_id = languages.id WHERE doctors_languages_map.doctor_id=:doctor_id"

WHERE_ID_DOCTORS = " WHERE id=:id RETURNING id"

QUERY_FOR_SPECIALISATION_MAP = "INSERT INTO doctors_specialisations_map VALUES (nextval('doctors_specialisations_map_id_seq'),:doctor_id,:specialisation_id) "


UPDATE_DOCTORS_SET = "UPDATE doctors SET "

INSERT_QUERY_FOR_TIMESLOT = " INSERT INTO doctors_time_slot VALUES (nextval('doctors_time_slot_id_seq'),:day,:video,:audio,:chat,:start_time,:end_time,:video_frequency,:audio_frequency,:chat_frequency,:is_available,:non_availability_reason,:is_active,now() at time zone 'UTC') RETURNING id; "