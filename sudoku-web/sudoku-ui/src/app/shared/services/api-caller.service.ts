import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from "@angular/common/http";
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiCallerService {

  private baseUrl: string = "http://localhost:3000";

  constructor(private readonly http: HttpClient) { }

  private getHeaders(): HttpHeaders {
    let headersConfig = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    return new HttpHeaders(headersConfig);
  }

  private getRequestOptions(params?: any): {} {
    let options = {
      headers: this.getHeaders(),
      observe: 'response'
    };
    if (params) {
      options["params"] = params;
    }
    return options;
  }

  public get(relativePath: string, params?: any): Observable<any> {
    console.log(this.baseUrl+relativePath);
    return this.http.get(this.baseUrl + relativePath, this.getRequestOptions(params)).pipe(map(
      (response: Response) => response.body
    ));
  }

  public post(relativePath: string, body: any): Observable<HttpResponse<any>> {
    console.log(this.baseUrl+relativePath);
    return this.http.post<any>(this.baseUrl + relativePath, body, this.getRequestOptions(null));
  }

  public upload(relativePath: string, body: any): Observable<HttpResponse<any>> {
    console.log(this.baseUrl+relativePath);
    return this.http.post<any>(this.baseUrl + relativePath, body);
  }

  public put(relativePath: string, body: any): Observable<any> {
    console.log(this.baseUrl+relativePath);
    return this.http.put(this.baseUrl + relativePath, body, this.getRequestOptions(null)).pipe(map(
      (response: Response) => response.body
    ));;
  }

  public delete(relativePath: string): Observable<HttpResponse<any>> {
    console.log(this.baseUrl+relativePath);
    return this.http.delete<any>(this.baseUrl + relativePath, this.getRequestOptions(null));
  }
}
