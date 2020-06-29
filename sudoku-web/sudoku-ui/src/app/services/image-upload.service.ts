import { Injectable } from '@angular/core';
import { ApiCallerService } from '../shared/services/api-caller.service';
import { Observable } from 'rxjs';
import { HttpResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ImageUploadService {

  constructor(private readonly apicaller: ApiCallerService) { }

  uploadImage(file):Observable<HttpResponse<any>> {
    return this.apicaller.upload('/upload', this.getFormData(file));
  }

  private getFormData(file: File): FormData {
    let formData = new FormData();
    formData.append("file", file);

    return formData;
  }
}
