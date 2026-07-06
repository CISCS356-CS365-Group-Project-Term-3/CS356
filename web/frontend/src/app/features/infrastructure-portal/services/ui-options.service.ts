import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_BASE = '/infra/rest';

@Injectable({
  providedIn: 'root'
})
export class UiOptionsService {

  constructor(private http: HttpClient) {}

  getUiOptions(): Observable<any> {
    return this.http.get<any>(`${API_BASE}/get_ui_options`);
  }

  addEncoderType(encoder: any) {
    return this.http.put(
      `${API_BASE}/encoder_types`,
      encoder
    );
  }

  toggleEncoderType(id: number, active: number) {
    return this.http.post(
      `${API_BASE}/encoder_types`,
      {
        id,
        active
      }
    );
  }

  deleteEncoderType(id: number) {
    return this.http.delete(
      `${API_BASE}/encoder_types`,
      {
        body: { id }
      }
    );
  }

  enableEncoder(id: number) {
    return this.http.post(
      `${API_BASE}/encoder_types`,
      {
        id,
        active: 1
      }
    );
  }

  disableEncoder(id: number) {
    return this.http.post(
      `${API_BASE}/encoder_types`,
      {
        id,
        active: 0
      }
    );
  }

  addCodec(codec: any) {
    return this.http.put(
      `${API_BASE}/codecs`,
      codec
    );
  }

  toggleCodec(id: number, active: number) {
    return this.http.post(
      `${API_BASE}/codecs`,
      {
        id,
        active
      }
    );
  }

  addTransmissionCondition(body: any) {
    return this.http.put(
      `${API_BASE}/transmission_conditions`,
      body
    );
  }

  toggleTransmissionCondition(body: any) {
    return this.http.post(
      `${API_BASE}/transmission_conditions`,
      body
    );
  }

  addSequence(sequence: any) {
    return this.http.put(
      `${API_BASE}/sequences`,
      sequence
    );
  }

  addVideoFile(videoFile: any) {
    return this.http.put(
      `${API_BASE}/video_files`,
      videoFile
    );
  }

  toggleSequence(body: {
    id: number;
    active: number;
  }) {
    return this.http.post(
      `${API_BASE}/sequences`,
      body
    );
  }
}
