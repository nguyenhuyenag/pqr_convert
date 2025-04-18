import concurrent.futures


# def run_method_on_parallel(func, data1, data2):
#     """
#         Run methods on 2 threads and return the results
#     """
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         future1 = executor.submit(func, data1)
#         future2 = executor.submit(func, data2)
#
#         result1, error1 = future1.result()
#         result2, error2 = future2.result()
#
#     if result1 and result2:
#         return result1, result2, None
#
#     return None, None, error1 or error2

def run_method_on_parallel(func, data1, data2):
    """
        Run func on two inputs in parallel and return the results and any error message.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(func, data1),
            executor.submit(func, data2)
        ]
        try:
            result1, error1 = futures[0].result()
            result2, error2 = futures[1].result()
        except Exception as e:
            return None, None, str(e)

    if error1 or error2:
        return None, None, error1 or error2

    return result1, result2, None
