import concurrent.futures

def run_parallel_on_fraction(func, numer, denom):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_numer = executor.submit(func, numer)
        future_denom = executor.submit(func, denom)

        numer_res, error_1 = future_numer.result()
        denom_res, error_2 = future_denom.result()

    if numer_res and denom_res:
        return numer_res, denom_res, None

    return None, None, error_1 or error_2
