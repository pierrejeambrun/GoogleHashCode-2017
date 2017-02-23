from itertools import islice

def read_input_file(name_of_my_file):
    line_count = 0;
    two_first_lines = read_slices(name_of_my_file, 0, 2)
    line_count += 2;
    caracteristics = two_first_lines[0].split(" ")
    total_endpoints_number = caracteristics[1]
    video_line_description = two_first_lines[1]
    endpoints_lines_description = []
    for endpoint in range(int(total_endpoints_number)):
        endpoint_line = read_slices(name_of_my_file, line_count, line_count + 1)
        number_of_caches_for_this_endpoint = int(endpoint_line[0].split(" ")[1])
        endpoints_lines_description.append(
            read_slices(name_of_my_file, line_count, line_count + number_of_caches_for_this_endpoint + 1))
        line_count += number_of_caches_for_this_endpoint + 1
    num_lines = sum(1 for line in open(name_of_my_file))
    requests_lines_description = read_slices(name_of_my_file, line_count, num_lines)
    return caracteristics, video_line_description, endpoints_lines_description, requests_lines_description

def read_slices(name_of_my_file, start, end):
    lines = []
    with open(name_of_my_file) as f:
        slice_ = islice(f, start, end)
        for line in slice_:
            lines.append(line.strip("\n"))
    return lines

def for_each_cache_find_the_endpoints_connected(endpoints_lines_description, number_of_caches):
    endpoints_connected_to_caches = [[] for i in range(number_of_caches)]
    for index_of_the_endpoint in range(len(endpoints_lines_description)):
        endpoint_description = endpoints_lines_description[index_of_the_endpoint]
        one_connection = 1
        while one_connection < len(endpoint_description):
            numerous = int(endpoint_description[one_connection].split(" ")[0])
            #     my_endpoints_list.append(numerous)
            # endpoints_connected_to_caches.append(my_endpoints_list)
            endpoints_connected_to_caches[numerous].append(index_of_the_endpoint)
            one_connection += 1
        my_endpoints_list = []
    return endpoints_connected_to_caches

def most_wanted_video_for_one_cache(connection_for_caches, requests_lines_description, number_of_videos):
    demand = [0 for i in range(number_of_videos)]
    for i in requests_lines_description:
        one_request = i.split(" ")
        one_request = map(lambda x: int(x), one_request)
        if one_request[1] in connection_for_caches:
            number_video = one_request[0]
            demand[number_video] += one_request[2]
    l = list(enumerate(demand))
    l.sort(key=lambda x: x[1], reverse=True)
    return l

def find_the_video_to_put_in_one_cache(ranked_videos_for_one_cache, max_cache_size, video_line_description):
    current_cache_size = 0
    video_for_this_cache = []
    video_size = map(lambda x: int(x), video_line_description.split(" "))
    for video in ranked_videos_for_one_cache:
        current_cache_size += video_size[video[0]]
        if current_cache_size < max_cache_size:
            video_for_this_cache.append(video[0])
        else:
            continue
    return video_for_this_cache

def calculate_cache_for_all_caches(input_file_path):
    final_result = []
    caracteristics, video_line_description, endpoints_lines_description, requests_lines_description = read_input_file(
        input_file_path)
    connection_for_caches = for_each_cache_find_the_endpoints_connected(endpoints_lines_description,
                                                                        int(caracteristics[3]))
    for connection in range(len(connection_for_caches)):
        ranked_videos_for_one_cache = most_wanted_video_for_one_cache(connection_for_caches[connection],
                                                                      requests_lines_description, int(caracteristics[0]))
        cache = find_the_video_to_put_in_one_cache(ranked_videos_for_one_cache, int(caracteristics[4]),
                                                   video_line_description)
        final_result.append(cache)
    return final_result

solution = calculate_cache_for_all_caches("input_me_at_the_zoo.in")
print solution

def write_solution_to_the_good_file(output_file_path, solution_to_write):
    with open(output_file_path, 'w') as f:
        f.write(str(len(solution)) + "\n")
        for index, line in enumerate(solution):
            f.write(str(index) + " ")
            f.write("".join(str(e) + " " for e in line) + "\n")
write_solution_to_the_good_file("output_me_at_the_zoo.txt", solution)
