#!/usr/bin/env python3
from itertools import count


def change(remaining,  options, id_gen=count()):
    if remaining <= 0:
        # draw this node
        local_node_id = next(id_gen)
        this_node_label = "{} remaining -".format(remaining)
        print('{}[label="{}"]'.format(local_node_id, this_node_label))
        return [[local_node_id]]
    else:
        all_results = []
        for i, this_option in enumerate(options):

            for chosen_amount in range(0, remaining + 1, this_option):

                new_remaining = remaining - chosen_amount

                not_this = [options[k] for k in range(len(options)) if k != i]
                # draw this node
                local_node_id = next(id_gen)
                times = chosen_amount // this_option
                this_node_label = "{} x ${} ({} remaining)(options {})".format(times, this_option, new_remaining, not_this)
                print('{}[label="{}"]'.format(local_node_id, this_node_label))

                new_change = change(new_remaining, not_this)

                # draw links from this node to descendents
                for child_path in new_change:
                    first_child = child_path[0]
                    print("{}->{}".format(local_node_id, first_child))

                this_amount_plus_change_for_remaining = [[local_node_id] + x for x in new_change]
                all_results.extend(this_amount_plus_change_for_remaining)
            else:
                local_node_id = next(id_gen)
                this_node_label = "{} remaining - No Range Available".format(remaining)
                print('{}[label="{}"]'.format(local_node_id, this_node_label))
                all_results.append([local_node_id])
        else:
            local_node_id = next(id_gen)
            this_node_label = "{} remaining - No Options Available".format(remaining)
            print('{}[label="{}"]'.format(local_node_id, this_node_label))
            return [[local_node_id]]

        return all_results


if __name__ == "__main__":
    print("digraph {")
    change_for_20 = change(10, [10, 5])
    print("}")
    for c in change_for_20:
        #print(c)
        pass
