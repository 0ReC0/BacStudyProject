def get_parameters_for_calculations(barriers_parameters, is_konf):
    if is_konf:
        global h
        h = int(input('Период обьективной конфиденциальности в неделях h (пример ответа: 1) : '))
    number_of_barriers = int(input('Количество преград: '))
    print('Заполните необходимые параметры преград:')
    for num in range(1, number_of_barriers + 1):
        u_m = int(input(f'Среднее возможное время преодоления преграды нарушителем u_m для преграды {num} в сутках: '))
        f_m = int(input(f'Среднее время между сменой регулируемого значения параметра f_m {num}-й преграды в сутках: '))
        parameters = {'idx': num, 'u_m': u_m, 'f_m': f_m}
        barriers_parameters.append(parameters)


def calculate_nsd_konf_m(u_m, f_m, h):
    nsd_konf_m = (1/u_m)/((1/u_m)+(1/h)+(1/f_m))
    return nsd_konf_m


def calculate_nsd_m(u_m, f_m):
    nsd_m = (1/u_m)/((1/u_m)+(1/f_m))
    return nsd_m


def calculate_probability_konf(barriers_parameters, probabilities):
    probability_nsd_mul = 1
    for barrier in barriers_parameters:
        u_m, f_m, idx = barrier.get('u_m'), barrier.get('f_m'), barrier.get('idx')
        nsd_conf_m = calculate_nsd_m(u_m, f_m)
        def_konf_m = 1 - nsd_conf_m
        probability_nsd_mul *= nsd_conf_m
        barrier_probability = {'idx': idx,
                               'nsd_m': nsd_conf_m,
                               'def_m': def_konf_m,
                               'probability_mul': 1 - probability_nsd_mul
                               }
        probabilities['barriers'].append(barrier_probability)
    probabilities['probability_konf'] = 1 - probability_nsd_mul


def calculate_probability_no_konf(barriers_parameters, probabilities):
    probability_nsd_mul = 1
    for barrier in barriers_parameters:
        u_m, f_m, idx = barrier.get('u_m'), barrier.get('f_m'), barrier.get('idx')
        nsd_m = calculate_nsd_m(u_m, f_m)
        def_m = 1 - nsd_m
        probability_nsd_mul *= nsd_m
        barrier_probability = {'idx': idx,
                               'nsd_m': nsd_m,
                               'def_m': def_m,
                               'probability_mul': 1 - probability_nsd_mul
                               }
        probabilities['barriers'].append(barrier_probability)
    probabilities['probability_konf'] = 1 - probability_nsd_mul


def print_probabilities(probabilities):
    barriers, probability_konf = probabilities['barriers'], probabilities['probability_konf'],
    for barrier in barriers:
        idx, nsd_m, def_m, probability_mul = barrier['idx'], barrier['nsd_m'], barrier['def_m'], barrier['probability_mul']
        print(f'Барьер {idx} P_НСД{".конф" if is_konf_mode else ""}_{idx} = {nsd_m:.4f}'
              f' P_ЗАЩ{".конф" if is_konf_mode else ""}_{idx} = {def_m:.4f} '
              f'P_ЗАЩ{".конф" if is_konf_mode else ""}_1-{idx} = {probability_mul:.4f}')
    print(f'P_{"конф" if is_konf_mode else "ЗАЩ"} = {probability_konf:.4f}')


if __name__ == '__main__':
    h = 0
    barriers_parameters = []
    is_konf_mode = bool(int(input('Режим конфиденциальности (0 - нет, 1 - да): ')))
    probabilities = dict({'probability_konf': 0, 'barriers': []})
    get_parameters_for_calculations(barriers_parameters, is_konf_mode)
    if is_konf_mode:
        calculate_probability_konf(barriers_parameters, probabilities)
    else:
        calculate_probability_no_konf(barriers_parameters, probabilities)
    print_probabilities(probabilities)




