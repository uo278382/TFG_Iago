import pandas as pd
import os
import glob

os.makedirs('2_datos_linea', exist_ok=True)

limpios = glob.glob('1_datos_limpios/*_1.csv')

for limpio_file in limpios:
    nombre_archivo = os.path.basename(limpio_file) 
    num_partido = nombre_archivo.split('_')[0]  
    events_file = f'0_datos_brutos/{num_partido}_events.csv'
    nombre_salida = nombre_archivo.replace('_1.csv', '_2.csv')
    output_file = os.path.join('2_datos_linea', nombre_salida)

    if not os.path.exists(events_file):
        print(f"Faltan eventos para el partido {num_partido}, se salta.")
        continue

    print(f"Procesando partido {num_partido}...")

    positions_data = pd.read_csv(limpio_file)
    events_data = pd.read_csv(events_file)

    event_duration = 5

    event_labels = {
        1: 'Tiro metido',
        2: 'Tiro fallado',
        3: 'Tiro libre',
        4: 'Rebote',
        5: 'Pérdida de balón',
        6: 'Falta',
        7: 'Falta grave',
        8: 'Sustitución',
        9: 'Tiempo muerto',
        10: 'Salto de inicio',
        12: 'Empiece de partido o de cuarto',
        13: 'Final de partido o de cuarto'
    }

    with open(output_file, mode='w', newline='') as file:
        writer = pd.DataFrame(columns=[
            'event_id', 'play_label', 'clase', 'event_time', 'game_clock', 'shot_clock',
            'x_loc_ball', 'y_loc_ball', 'z_loc_ball',
            'team_id_home',
            'player_id_player_1', 'x_loc_player_1', 'y_loc_player_1',
            'player_id_player_2', 'x_loc_player_2', 'y_loc_player_2',
            'player_id_player_3', 'x_loc_player_3', 'y_loc_player_3',
            'player_id_player_4', 'x_loc_player_4', 'y_loc_player_4',
            'player_id_player_5', 'x_loc_player_5', 'y_loc_player_5',
            'team_id_away',
            'player_id_player_6', 'x_loc_player_6', 'y_loc_player_6',
            'player_id_player_7', 'x_loc_player_7', 'y_loc_player_7',
            'player_id_player_8', 'x_loc_player_8', 'y_loc_player_8',
            'player_id_player_9', 'x_loc_player_9', 'y_loc_player_9',
            'player_id_player_10', 'x_loc_player_10', 'y_loc_player_10'
        ]).to_csv(file, index=False, header=True)





        for _, event in events_data.iterrows():
            event_id = event['EVENTNUM']
            event_positions = positions_data[positions_data['event_id'] == event_id]

            print("El evento "+str(event_id)+" tiene "+str(len(event_positions)/11)+" instantes")

            if len(event_positions) < 25 * 11 * 5:
                print(f"Evento {event_id} no tiene los suficientemente instantes")
                continue

            if (len(event_positions)>0):
            
                minuto = event['PCTIMESTRING']
                event_period = event['PERIOD']
                event_type = event['EVENTMSGTYPE']

                if event_type == 1:
                    clase = 1 
                elif event_type in [2, 4]:
                    clase = 2 
                elif event_type == 5:
                    clase = 3  
                else:
                    clase = 0  


                play_label = event_labels.get(event_type, 'Indefinido')

                partes = minuto.split(":")
                event_time = int(partes[0]) * 60 + int(partes[1])
                print("El evento paso en el minuto "+str(float(event_time)))
                
                num_instantes = event_duration * 25 * 11

                print(len(event_positions))





                num_min = event_positions[event_positions['game_clock'] <= float(event_time)]

                if (len(num_min)>0):
                    num_min_index = num_min.index

   
                    num_min_3 = num_min_index[0]-25*11*3

                    if (num_min_3<event_positions.index[0]):
                        print("Se descarta el evento "+str(event_id)+" porque no tiene 3 segundos para atras")
                        continue
                    else:
                        start_index = num_min_3
                    
                    end_index = start_index + 25*11*5

                    if (end_index>event_positions.index[-1]):
                        print("Se descarta el evento "+str(event_id)+" porque no tiene 2 segundos para alante")
                        continue

                    print("El primer index es "+str(start_index)+" y el ultimo es "+str(end_index))

                    start_index_mod=start_index-event_positions.index[0]
                    end_index_mod=start_index_mod + 25*11*5




                    if (event_positions.index[0]+len(event_positions)>=end_index):

                        sequence_positions = event_positions.iloc[start_index_mod:end_index_mod]
                        cont_player=0


                        for _, row in sequence_positions.iterrows():
                            if row['team_id'] == -1: 
                                sequence_data = {
                                    'event_id': event_id,
                                    'play_label': play_label,
                                    'clase': clase,
                                    'event_time': minuto,
                                    'game_clock': row['game_clock'],
                                    'shot_clock': row['shot_clock'],
                                    'x_loc_ball': row['x_loc'],
                                    'y_loc_ball': row['y_loc'],
                                    'z_loc_ball': row['radius']
                                }
                            else: 

                                if cont_player==0:

                                    sequence_data[f'team_id_home'] = row['team_id']
                                elif cont_player==5:

                                    sequence_data[f'team_id_away'] = row['team_id']

                                sequence_data[f'player_id_player_{cont_player+1}'] = row['player_id']
                                sequence_data[f'x_loc_player_{cont_player+1}'] = row['x_loc']
                                sequence_data[f'y_loc_player_{cont_player+1}'] = row['y_loc']
                                cont_player=cont_player+1
                            



                            if cont_player==10:

                                pd.DataFrame(sequence_data, index=[0]).to_csv(file, index=False, header=False)
                                cont_player=0
                        
                        print("Evento "+str(event_id)+" terminado")