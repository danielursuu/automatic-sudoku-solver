import { Component, OnInit } from '@angular/core';
import { ImageUploadService } from '../services/image-upload.service';

@Component({
  selector: 'app-image-uploader',
  templateUrl: './image-uploader.component.html',
  styleUrls: ['./image-uploader.component.css']
})
export class ImageUploaderComponent implements OnInit {

  uploadedFiles: any[] = [];

  constructor(private readonly imageUploadService:ImageUploadService) { }

  ngOnInit(): void {
  }

  onUpload(event) {
    for (let file of event.files) {
      this.uploadedFiles.push(file);
    }
    console.log(this.uploadedFiles);

  }

  onUploadHandler(event){
    console.log(event.files[0]);
    
    this.imageUploadService.uploadImage(event.files[0]).subscribe((response)=>console.log(response),(error)=>console.log(error));
    
  }

}
