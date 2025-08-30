// Include the header file to get access to the MicroPython API
#include "py/dynruntime.h"
#include <math.h>
#include "py/obj.h"
#include "py/runtime.h"
#include "py/builtin.h"
#include "py/objlist.h"
#include "py/objarray.h"
#include <string.h>
#include <stdlib.h>

// Helper: convert mp_obj_t to int array
static void extract_int_array(mp_obj_t obj, uint16_t **out_arr, uint16_t *out_len) {
    
    
    mp_buffer_info_t bufinfo;
    // Try to use buffer protocol first (array, bytes, bytearray, memoryview)
    if (mp_get_buffer(obj, &bufinfo, MP_BUFFER_READ)) {
        *out_len = bufinfo.len / sizeof(uint16_t);
        uint16_t *arr = m_new(uint16_t, *out_len);
        memcpy(arr, bufinfo.buf, *out_len * sizeof(int));
        *out_arr = arr;
        return;
    }

    // If it's a list
    if (mp_obj_is_type(obj, &mp_type_list)) {
        mp_obj_list_t *list = MP_OBJ_TO_PTR(obj);
        *out_len = list->len;
        uint16_t *arr = m_new(uint16_t, *out_len);
        for (size_t i = 0; i < *out_len; i++) {
            arr[i] = mp_obj_get_int(list->items[i]);
        }
        *out_arr = arr;
        return;
    }

    // Otherwise, raise error
    mp_raise_TypeError(MP_ERROR_TEXT("expected list, array, or bytes"));
}

static float apply_biquad( float input_sample, float *filter_coefs, float*hidden_state)  {
    //declare output
    float output_sample;
    //compute output
    output_sample = filter_coefs[0] * input_sample + hidden_state[0];
    //update hidden states
    hidden_state[0]= filter_coefs[1] * input_sample - filter_coefs[3] * output_sample + hidden_state[1];
    hidden_state[1] = filter_coefs[2] * input_sample - filter_coefs[4] * output_sample;
    return output_sample;
}

static int16_t saturate_q15(float x)
{
    if (x < -(1<<15))
    {
        x = -(1<<15);
    }
    else if (x > (1<<15) - 1)
    {
        x = (1<<15) - 1;
    }
    return (int16_t)x;
}

/* static float normalize_q15(int x)
{   
    float y = (float)(x + 32768.0f)/(32767 + 32768);

    return y;
}*/

//filter data

/*
static int16_t filter_data_online(uint16_t x, float **filter_matrix, float *hidden_state)  {

    float y = x;
    for (int j = 0; j < 5; j++)
        {       
            y = apply_biquad( y, *(filter_matrix + j ), (hidden_state + 2*j ));
        }
    return saturate_q15(y); 
}
*/

static void filter_data_postprocessing(uint16_t * input_data, int16_t *output_data, float filter_matrix[5][5], float *hidden_states, uint16_t num_samples)  {
 
    for (uint16_t i = 0; i <  num_samples; i++)
    {   
        float out_sample = (float)input_data[i];
        for (uint8_t j = 0; j < 5; j++)
        {       
            out_sample= apply_biquad( out_sample, *(filter_matrix + j), (hidden_states + 2*j));
        }
        out_sample = saturate_q15(out_sample);
        output_data[i] = out_sample;
    }
}

// This is the function which will be called from Python, as factorial(x)
static mp_obj_t filter_biquad_cascade(mp_obj_t mp_obj_data) {

   
    uint16_t *raw_sensor_data;
    uint16_t num_samples;
    // Extract samples
    extract_int_array(mp_obj_data, &raw_sensor_data, num_samples);

    //Define coefficients
    float biquad_layers[5][5] = {{5.49496377e-04, -1.09899275e-03,  5.49496377e-04 , 7.75752801e-01,  5.82317689e-01},
                                {1.00000000e+00, -2.00000000e+00,  1.00000000e+00, 5.54213901e-01,  6.30454831e-01},
                                {1.00000000e+00,  0.00000000e+00, -1.00000000e+00, 1.03575406e+00,  6.80934131e-01},
                                {1.00000000e+00,  2.00000000e+00,  1.00000000e+00, 4.52443546e-01,  8.39682131e-01},
                                {1.00000000e+00,  2.00000000e+00,  1.00000000e+00, 1.26801640e+00,  8.75731512e-01},
                                };


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
// Define a Python reference to the function above
static MP_DEFINE_CONST_FUN_OBJ_1(filter_biquad_cascade_obj, filter_biquad_cascade);

// This is the entry point and is called when the module is imported
mp_obj_t mpy_init(mp_obj_fun_bc_t *self, size_t n_args, size_t n_kw, mp_obj_t *args) {
    // This must be first, it sets up the globals dict and other things
    MP_DYNRUNTIME_INIT_ENTRY

    // Make the function available in the module's namespace
    mp_store_global(MP_QSTR_filter_biquad_cascade, MP_OBJ_FROM_PTR(&filter_biquad_cascade_obj));


    // This must be last, it restores the globals dict
    MP_DYNRUNTIME_INIT_EXIT
}