// import { Injectable } from '@angular/core';
// import { ApiCallerService } from './api-caller.service';
// import { Task } from 'src/app/shared/models/task';
// import { Observable } from 'rxjs';

// @Injectable({
//   providedIn: 'root'
// })
// export class TaskService {

//   static readonly API_BASE_PATH: string = "/task";

//   constructor(private readonly apiCaller: ApiCallerService) { }

//   getAll(): Promise<Task[]> {
//     return this.apiCaller.get(TaskService.API_BASE_PATH).toPromise();
//   }

//   create(task: Task): Observable<any> {
//     return this.apiCaller.post(TaskService.API_BASE_PATH + "/add", task);
//   }

//   delete(id: number): Observable<any> {
//     return this.apiCaller.delete(TaskService.API_BASE_PATH + "/" + id);
//   }

//   updateStatus(task: Task): Promise<Task> {
//     return this.apiCaller.put(TaskService.API_BASE_PATH + "/update", task).toPromise();
//   }
// }
