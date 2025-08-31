int main() {
    // Your code here
    return 0;
}

// This is the function which will be called from Python, as factorial(x)
static mp_obj_t filter_biquad_cascade(mp_obj_t mp_obj_data) {

   
    uint16_t *raw_sensor_data;
    uint16_t num_samples;
    // Extract samples
    extract_int_array(mp_obj_data, &raw_sensor_data, num_samples);

    int16_t *output_filter_data = (int16_t*)malloc(*num_samples * sizeof(int16_t));
    float *hidden_states = (float*)malloc(10 * sizeof(float));
    if (hidden_states == NULL) {
         mp_raise_TypeError(MP_ERROR_TEXT("malloc failed"));
    }
    memset(hidden_states, 0, 10 * sizeof(float));
    filter_data_postprocessing(raw_sensor_data, output_filter_data, biquad_layers,hidden_states, *num_samples);
    
    //create a list mp object 
    mp_obj_t result_list = mp_obj_new_list(*num_samples, NULL);
    for (size_t i = 0; i < *num_samples; i++) {
    ((mp_obj_list_t*)MP_OBJ_TO_PTR(result_list))->items[i] = mp_obj_new_int(output_filter_data[i]);
    }
    
    free(raw_sensor_data);
    free(output_filter_data);
    free(hidden_states);
    // Convert the result to a MicroPython integer object and return it
    return result_list;
}