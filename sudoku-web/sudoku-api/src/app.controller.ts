import { Controller, Get, Post, UseInterceptors, UploadedFile, Param, Res } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';

import { AppService } from './app.service';
import { imageFileFilter, editFileName } from './utils/image-uploading.utils';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) { }

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Post()
  @UseInterceptors(
    FileInterceptor('image', {
      storage: diskStorage({
        destination: './images',
        filename: editFileName
      }),
      fileFilter: imageFileFilter
    })
  )
  async uploadImage(@UploadedFile() file) {
    const response = {
      originalName: file.originalname,
      fileName: file.filename
    };
    return response;
  }

  @Get(':path')
  getUploadedImage(@Param('path') path, @Res() res){
    return res.sendFile(path,{root:'./images'});
  }
}
