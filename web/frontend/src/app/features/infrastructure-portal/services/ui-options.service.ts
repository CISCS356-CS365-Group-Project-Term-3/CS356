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
    return this.http.post(
      'http://localhost:5001/rest/encoder_types',
      encoder
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
}
