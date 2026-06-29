import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class UiOptionsService {

  private apiUrl = 'http://localhost:5001/rest/get_ui_options';

  constructor(private http: HttpClient) {}

  getUiOptions(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }

  addEncoderType(encoder: any) {
    return this.http.put(
      'http://localhost:5001/rest/encoder_types',
      encoder
    );
  }

  toggleEncoderType(id: number, active: number) {
    return this.http.post(
      'http://localhost:5001/rest/encoder_types/active',
      {
        id,
        active
      }
    );
  }

  deleteEncoderType(id: number) {
    return this.http.delete(
      'http://localhost:5001/rest/encoder_types',
      {
        body: { id }
      }
    );
  }

  enableEncoder(id: number) {
    return this.http.post(
      'http://localhost:5001/rest/encoder_types',
      {
        id,
        active: 1
      }
    );
  }

  disableEncoder(id: number) {
    return this.http.post(
      'http://localhost:5001/rest/encoder_types',
      {
        id,
        active: 0
      }
    );
  }

  addCodec(codec: any) {

    return this.http.put(

      'http://localhost:5001/rest/codecs',

      codec

    );

  }
  toggleCodec(id: number, active: number) {
    return this.http.post(

      'http://localhost:5001/rest/codecs/active',

      {
        id,
        active
      }

    );

  }

  addTransmissionCondition(body: any) {

    return this.http.put(

      'http://localhost:5001/rest/transmission_conditions',

      body

    );

  }

  toggleTransmissionCondition(body: any) {

    return this.http.post(
      'http://localhost:5001/rest/transmission_conditions/active',

      body
    );
  }

  addSequence(sequence: any) {

    return this.http.post(

      `http://localhost:5001/rest/sequences`,

      sequence

    );

  }

  toggleSequence(body: {

    id: number;

    active: number;

  }) {

    return this.http.post(

      `http://localhost:5001/rest/sequences/active`,

      body

    );

  }

}
